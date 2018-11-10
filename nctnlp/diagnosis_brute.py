from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd

with open('diagnosis.csv',encoding='utf-8') as diagnosis_file:
    diagnosis_data = pd.read_table(diagnosis_file)


diagnosis_list = diagnosis_data['data'].str.lower()
codes_list = diagnosis_data['label'].values
type(diagnosis_list)
print("Found: ",diagnosis_list[diagnosis_list == 'Rectal Adenocarcinoma'.lower()].index[0])
def get_codes(data):
    array = []
    for idx in diagnosis_list[diagnosis_list == data.lower()].index:
        array.append(codes_list[idx])
    return array

output_file = open('nct_to_diagnosis.csv','w',encoding='utf-8')
pwd = Path('./NCT')
unfound = 0
total = 0
for file in pwd.iterdir():
    if str(file).startswith('NCT') and str(file).endswith('.xml'):
        with open(file,encoding='utf-8') as infile:
            print("Working on",str(file))
            contents = infile.read()
            soup = BeautifulSoup(contents, 'xml')
            data = soup.find_all('condition')
            codes = []
            for condition in data:
                codes += get_codes(condition.get_text())
            total += 1
            if not codes:
                unfound += 1
            output_file.write(str(file)[4:-4] + '\t' + '|'.join(set(codes)) + '\n')

print("Percent diagnosed:",str(100*unfound/total) + '%')
output_file.close()