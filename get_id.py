import xml.etree.ElementTree as ET
import csv
import re

root = ET.parse('Dataset_name_Interesting.xml').getroot()
# root = ET.parse('test.xml').getroot()
header = ['', 'name', 'id', 'text']
ids = []
count = 0
offset = 100
for tei in root.findall('TEI'):
    for p in tei.findall('text/body/p'):
        text = ''.join(p.itertext())
        indices = []
        software_list = []
        id_list = []
        not_soft_list = []
        for software in p.findall('rs'):
            if software.attrib['type'] == 'software':
                # print('yes')
                # print(software.text)
                if not software.text in software_list:
                    soft_indices = [m.start()
                                    for m in re.finditer(re.escape(software.text), text)]
                    indices = indices + soft_indices
                    indices.sort()
                id = software.attrib['{http://www.w3.org/XML/1998/namespace}id']
                software_list.append(software.text)
                id_list.append(id)
        for i in range(len(software_list)):
            index = indices[i]
            name = software_list[i]
            id = id_list[i]
            data = [count, name, id, text[index-offset if index >
                                          offset else index:index+offset]]
            ids.append(data)
            count += 1
print(count)
# print(data)
with open('software_data.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    writer.writerow(header)

    writer.writerows(ids)
