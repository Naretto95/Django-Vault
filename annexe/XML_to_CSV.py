from cpe import CPE
import csv
import untangle
from tqdm import tqdm

obj = untangle.parse("official-cpe-dictionary_v2.3.xml")
items = obj.cpe_list.cpe_item
del obj

with open('cpes.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["name", "reference"])
    for item in tqdm(items) :
        obj = CPE(item.cpe_23_cpe23_item["name"])
        reference = obj.as_fs()
        name = obj.get_product()[0] + ":" + obj.get_version()[0] + ":" + obj.get_update()[0] + ":" + obj.get_edition()[0] + ":" + obj.get_language()[0] + ":" + obj.get_vendor()[0]
        writer.writerow([name, reference])   

