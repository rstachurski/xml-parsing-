from csv import writer
from sys import flags
import xml.etree.ElementTree as ET
import csv
import re
import enchant
def remove(string):
    return string.replace(" ", "")

def increase(type, dict):
     dict[type] = dict.get(type,0) + 1

count = {'multiword' : 0 , 'allcaps' : 0, 'nocaps':0,'firstcap' : 0 , 'firstuncap' : 0}
multi_count = {'multiword types':{'allcaps' : 0, 'nocaps':0,'firstcap' : 0 , 'firstuncap' : 0}}
total = 0
has_nonalpha = 0
software = {}
nonalpha = {}
groups = {}
root =  ET.parse('softcite_corpus-full.tei.xml').getroot()
p = '[A-Z]+[a-z]+$'  

for type in root.findall('TEI/text/body/p/rs'):
    if type.attrib['type'] == 'software':
        notgrouped = 1
        software[type.text] =  software.get(type.text, 0) + 1
        total += 1
        for name in groups:
            if enchant.utils.levenshtein(type.text, name) < 3:
                notgrouped = 0
                if len(groups) != 0 and len(groups[name])!= 0:
                    groups[name][0] = int(groups[name][0]) + 1
                if not type.text in groups[name]:
                    groups[name].append(type.text)
                break
        if notgrouped == 1:
            groups[type.text] = [1,type.text]
            # groups[type.text] = [type.text]
        if not remove(type.text).isalnum():
            has_nonalpha += 1
            for c in remove(type.text):
                if not c.isalnum():
                    nonalpha[c] = nonalpha.get(c,0) + 1
        if type.text[0].isupper():
            if type.text.isupper():
                increase('allcaps', count)
            else:
                increase('firstcap', count)
        else:
            if(re.search(p, type.text)):
                increase('firstuncap', count)
            else:
                increase('nocaps', count)
        
        if len(type.text.split()) != 1:
            increase('multiword', count)
            if type.text[0].isupper():
                if type.text.isupper():
                    increase('allcaps', multi_count['multiword types'])
                else:
                    increase('firstcap', multi_count['multiword types'])
            else:
                if(re.search(p, type.text)):
                    increase('firstuncap', multi_count['multiword types'])
                else:
                    increase('nocaps', multi_count['multiword types'])

file = open("softwarename.csv", "w", encoding="utf-8")
print(count)
print(total)
print(multi_count)
print(has_nonalpha)
print(nonalpha)
write = csv.writer(file)
for i in sorted(software):
    write.writerow([i, software[i]])
file.close()

with open("softwarenamegroups.txt", 'w', encoding="utf-8") as f: 
    for key, value in groups.items(): 
        f.write('%s:%s\n' % (key, value))
    for key, value in count.items(): 
        f.write('%s:%s\n' % (key, value))
    for key, value in multi_count.items(): 
        f.write('%s:%s\n' % (key, value))
    for key, value in nonalpha.items(): 
        f.write('%s:%s\n' % (key, value))
    f.write("Total names%i:" % total)
    f.write("Total names with non alphanumeric character: %i" % has_nonalpha)