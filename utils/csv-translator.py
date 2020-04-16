import numpy as np 
import pandas as pd 
import re
from string import punctuation
import requests

recipes=pd.read_csv('../data/mydata.csv')

#recipes["Text"] = recipes["name"] + ' ' + recipes["description"]
#recipes = recipes.drop(['id', 'minutes','contributor_id', 'nutrition', 'n_steps', 'n_ingredients', 'submitted', 'name', 'description', 'steps', 'ingredients'], axis=1)
mini = recipes.head(20000)

auth = ''

#for i in mini.Text:
#    string = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=' + auth + '&text=' + i + '&lang=en-ru'
#    r = requests.get(string)
#    b = r.text[36:]
#    b = b.strip('"]}')
#    print(b)

counter = 0
    
def text_translator(text):
    global counter
    string = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=' + auth + '&text=' + text + '&lang=en-ru'
    r = requests.get(string)
    text = r.text[36:]
    text = text.strip('"]}')
    text = re.sub("," , "", text)
    counter += 1
    print(counter)
    return text
    
mini.Text = mini.Text.apply(lambda x: text_translator(x))

mini.to_csv('../data/mini.csv')

