import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from bs4 import BeautifulSoup
import json
from pprint import pprint

with open('diagnosis.json') as json_data:
    d = json.load(json_data)
    json_data.close()


infile = open("NCT00321685.xml", "r")
contents = infile.read()
soup = BeautifulSoup(contents, 'xml')
data = soup.find_all('condition')

all_txt = ''
txt_array = []

for info in data:
    txt_array.append(info.get_text())
all_txt = ' '.join(txt_array)
print(all_txt)
df = pd.read_table('diagnosis.csv')

array = df['label'].values
print(array[0])

int_dict = {}
dict_int = {}
idx = 0
for item in array:
    if item in int_dict:
        pass
    else:
       dict_int[idx] = item
       int_dict[item] = idx
       idx += 1

df['int_labels'] = df['label'].map(int_dict)

print(df.loc[0])

y = df['int_labels'].values
count_vectorizer = CountVectorizer(decode_error='ignore', stop_words='english', max_df=0.2)
x = count_vectorizer.fit_transform(df['data'])
print(count_vectorizer.get_stop_words())

tfidf = TfidfVectorizer(decode_error='ignore', stop_words='english', max_df=0.8)
x = tfidf.fit_transform(df['data'])



model = MultinomialNB()
model.fit(x, y)


data_vectorizer = CountVectorizer(vocabulary=count_vectorizer.get_feature_names())
print(count_vectorizer.get_feature_names())
xml_x = data_vectorizer.fit_transform(txt_array)

data_tfidf = TfidfVectorizer(vocabulary=tfidf.get_feature_names())
xml_x = data_tfidf.fit_transform(txt_array)


predictions = model.predict(xml_x)
for predicted, txt in zip(predictions,txt_array):
    print(txt + ':',dict_int[predicted])

