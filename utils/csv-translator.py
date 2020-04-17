import numpy as np
import pandas as pd
import re
from string import punctuation
import requests

recipes = pd.read_csv('../data/mydata.csv')

mini = recipes.head(20000)

auth = ''

counter = 0


def text_translator(text):
    global counter
    string = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=' + \
        auth + '&text=' + text + '&lang=en-ru'
    r = requests.get(string)
    text = r.text[36:]
    text = text.strip('"]}')
    text = re.sub(",", "", text)
    counter += 1
    print(counter)
    return text


mini.Text = mini.Text.apply(lambda x: text_translator(x))

mini.to_csv('../data/mini.csv')
