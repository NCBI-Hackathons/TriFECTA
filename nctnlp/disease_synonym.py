import requests
from bs4 import BeautifulSoup
import json

proxies = {
    'http': 'http://proxy.swmed.edu:3128',
    'https': 'https://proxy.swmed.edu:3128',
}
# nci = requests.get('https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&code=C3106',
#                    proxies=proxies)
# parsed = BeautifulSoup(nci.text, 'html5lib')
#
# tags = parsed.findAll("table", class_="datatable_960")
# synonyms = tags[0].findAll('td')
# for item in synonyms:
#     print(item.get_text())

with open('oncotree.json') as oncotree_file:
    oncotree = json.loads(oncotree_file.read())

nci_dict = {}
print(oncotree[0])
non_unique = 0
missing = 0
for item in oncotree:
    try:
        nci = item['externalReferences']['NCI'][0]
    except KeyError:
        missing += 1
        continue
    print(nci)
    if nci in nci_dict:
        non_unique += 1
        nci_dict[nci] += ('&' + item['code'])
    else:
        nci_dict[nci] = item['code']
print(nci_dict)
print(len(nci_dict))
print("Missing:", missing)
print("Not Unique:", non_unique)
BASE_URL = 'https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&code='
diagnosis = {}
diagnosis_file = open('diagnosis.txt', 'w', encoding='utf-8')
idx = 0
for key, val in nci_dict.items():
    idx += 1
    print('Retrieving synonyms for',str(idx) + ':',key)
    response = requests.get(BASE_URL + key, proxies=proxies)
    soup = BeautifulSoup(response.text, 'html5lib')
    synonyms = soup.find_all('table', class_='datatable_960')[0].find_all('td')
    diagnosis[val] = [x.get_text() for x in synonyms]
    array = [val] + diagnosis[val]
    diagnosis_file.write('\t'.join(array) + '\n')
diagnosis_file.close()

print(diagnosis)
