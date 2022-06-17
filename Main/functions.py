from .models import *
from django.db.models import Max
import random

def get_random_obj_from_queryset(queryset):
    max_pk = queryset.aggregate(max_pk=Max("pk"))['max_pk']
    while True:
        obj = queryset.filter(pk=random.randint(1, max_pk)).first()
        if obj:
            return obj

def populatedb():
    user = User.objects.get(username="admin")
    extension = Extension.objects.get(user=user)
    for i in range(30):
        group = Group.objects.create(extension=extension, name="Group"+str(i), description="Description of group"+str(i))
        for j in range(10):
            asset = Asset.objects.create(group=group, name="Asset"+str(j), description="Description of asset"+str(j))
            for k in range(10):
                cpe = get_random_obj_from_queryset(CPE.objects.all())
                Software.objects.create(asset=asset, name="Software"+str(k), description="Description of software"+str(k), version="1.0.0", cpe=cpe)