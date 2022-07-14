from .models import *
from django.db.models import Max
import os
import random
import gzip
import requests
from cpe import CPE as CPElib
from io import BytesIO
from django.conf import settings
import untangle
from tqdm import tqdm

def get_random_obj_from_queryset(queryset):
    max_pk = queryset.aggregate(max_pk=Max("pk"))['max_pk']
    while True:
        obj = queryset.filter(pk=random.randint(1, max_pk)).first()
        if obj:
            return obj

def testdb():
    user = User.objects.get(username="admin")
    extension = Extension.objects.get(user=user)
    print("Deleting previous objects...")
    Group.objects.all().delete()
    Asset.objects.all().delete()
    print("Creating objects...")
    for i in tqdm(range(30)):
        group = Group.objects.create(extension=extension, name="Group"+str(i), description="Description of group"+str(i))
        for j in range(10):
            asset = Asset.objects.create(group=group, name="Asset"+str(j), description="Description of asset"+str(j))
            for k in range(10):
                cpe = get_random_obj_from_queryset(CPE.objects.all())
                Software.objects.create(asset=asset, name="Software"+str(k), description="Description of software"+str(k), version="1.0.0", cpe=cpe)

def populatecpedb():
    NVD_CPE_URL = ("https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.gz")

    print("Reading file...")
    resp = requests.get(NVD_CPE_URL,timeout=120).content
    open(os.path.join(settings.TMP,"official-cpe-dictionary_v2.3.xml"), "wb").write(gzip.GzipFile(fileobj=BytesIO(resp)).read())
    obj = untangle.parse(os.path.join(settings.TMP,"official-cpe-dictionary_v2.3.xml"))
    items = obj.cpe_list.cpe_item
    del obj

    print("Importing cpes...")
    for item in tqdm(items) :
        obj = CPElib(item.cpe_23_cpe23_item["name"])
        elements = [obj.get_product()[0],obj.get_version()[0],obj.get_update()[0],obj.get_edition()[0],obj.get_software_edition()[0],obj.get_language()[0],obj.get_target_software()[0],obj.get_target_hardware()[0], obj.get_other()[0]]
        reference = obj.as_fs()
        name = obj.get_vendor()[0]
        for element in elements :
            if element != "*":
                name += " " + element
        if obj.get_part()[0] != "a" :
            name += " Part:" + obj.get_part()[0]
        CPE.objects.get_or_create(name=name, reference=reference)
        
    print("Removing file...")
    os.remove(os.path.join(settings.TMP,"official-cpe-dictionary_v2.3.xml"))
