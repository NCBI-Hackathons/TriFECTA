from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
from pymongo import MongoClient

with open('genes.tsv',encoding='utf-8') as gene_file:
    gene_data = pd.read_table(gene_file)


client = MongoClient('localhost', 27017)
gene_list = gene_data['Synonyms'].values
print(gene_list)
symbols_list = gene_data['Gene Symbol'].values
def get_gene(data):
    genes = []
    for idx,symbol in enumerate(symbols_list):
        symbol = ' ' + symbol.strip()
        if len(symbol) == 3:
            symbol = symbol + ' '
        found = data.find(symbol)
        if found != -1:
            genes.append(symbol)
    for idx,synonyms in enumerate(gene_list):
        try:
            for synonym in synonyms.split(','):
                if not synonym.isdigit():
                    synonym = ' ' + synonym.strip()
                if len(synonym) == 3:
                    synonym = synonym + ' '
                if not synonym.strip().isdigit():
                    found = data.find(synonym)
                else:
                    found = -1
                if found != -1:
                    print("Found synonym",synonym)
                    genes.append(symbols_list[idx])
        except AttributeError:
            pass
    return genes

output_file = open('nct_to_genes.csv','w',encoding='utf-8')
pwd = Path('./NCT')
unfound = 0
total = 0
for file in pwd.iterdir():
    if str(file).startswith('NCT') and str(file).endswith('.xml'):
        with open(file,encoding='utf-8') as infile:
            print("Working on",str(file))
            contents = infile.read()
            soup = BeautifulSoup(contents, 'xml')
            data = soup.find_all()
            all_text = []
            for text in data:
                all_text.append(text.get_text())
            gene_symbols = get_gene(" ".join(all_text))
            total += 1
            if not gene_symbols:
                unfound += 1
            output_file.write(str(file)[4:-4] + '\t' + '|'.join(set(gene_symbols)) + '\n')

print("Percent containing genes:",str(100*(1-unfound/total)) + '%')
output_file.close()