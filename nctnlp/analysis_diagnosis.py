import json
with open('diagnosis.txt', encoding="utf-8") as diagnosis_file:
    diagnosis = diagnosis_file.readlines()

fpout = open('diagnosis.csv','w', encoding='utf-8')

header = 'label\tdata\n'
fpout.write(header)
for line in diagnosis:
    array = line.strip().split('\t')
    out_array = [array[0]]
    for item in array[1:]:
        fpout.write(array[0] + '\t' + '"' + item + '"' + '\n')
