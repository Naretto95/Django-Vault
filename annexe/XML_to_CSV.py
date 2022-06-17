from cpe import CPE
import csv
import untangle
from tqdm import tqdm

print("Reading file...")
obj = untangle.parse("official-cpe-dictionary_v2.3.xml")
items = obj.cpe_list.cpe_item
del obj

with open('cpes.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["name", "reference"])
    for item in tqdm(items) :
        obj = CPE(item.cpe_23_cpe23_item["name"])
        elements = [obj.get_version()[0],obj.get_update()[0],obj.get_edition()[0],obj.get_software_edition()[0],obj.get_language()[0],obj.get_vendor()[0],obj.get_target_software()[0],obj.get_target_hardware()[0], obj.get_other()[0]]
        reference = obj.as_fs()
        name = obj.get_product()[0]
        for element in elements :
            if element != "*":
                name += " " + element
        if obj.get_part()[0] != "a" :
            name += " Part:" + obj.get_part()[0]
        writer.writerow([name, reference])

