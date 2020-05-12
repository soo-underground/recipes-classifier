# -*- coding: utf-8 -*-
from nltk.stem import WordNetLemmatizer
import flask
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import pickle
import nltk
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import f1_score
import requests
from string import punctuation

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

with open('YaTranslateKey.key', 'r') as file:
    auth = file.read().replace('\n', '')  #reading api key for machine translation of texts

# functions that read pickled ml models
def load_classifier():
    classifier = pickle.load(open('models/multilabel_model.sav', 'rb'))
    return classifier


def load_tfidf():
    tfidf = pickle.load(open('models/tfidf.sav', 'rb'))
    return tfidf


def load_binarizer():
    binarizer = pickle.load(open('models/multilabel_binarizer.sav', 'rb'))
    return binarizer

# functions that preprocess text
def clean_text(text):
    text = re.sub("\'", "", text)
    text = re.sub("[^a-zA-Z]", " ", text)
    text = ' '.join(text.split())
    text = text.lower()
    return text


wordnet_lemmatizer = WordNetLemmatizer()


def lemmatize_text(text):
    lemmatized_text = []
    sentence_words = nltk.word_tokenize(text)
    for word in sentence_words:
        lemmatized_text.append(wordnet_lemmatizer.lemmatize(word, pos="v"))
    lemmatized_text = ' '.join(lemmatized_text)
    return lemmatized_text


nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))


def remove_stopwords(text):
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)

# main endpoint
@app.route('/predict', methods=['POST'])
def predict():
    global auth #using yandex.translate api key
    request_json = request.get_json()
    x = str(request_json['input'])
    string = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=' + \
        auth + '&text=' + x + '&lang=ru-en'
    r = requests.get(string)
    text = r.text[36:] #quick hack used instead of parsing ya.translate json
    text = text.strip('"]}') #quick hack used instead of parsing ya.translate json
    text = re.sub(",", "", text)
    x = text
    print(x) #print for heroku logs

    classifier = load_classifier()
    tfidf = load_tfidf()
    binarizer = load_binarizer()
    x = clean_text(x)
    x = remove_stopwords(x)
    x = lemmatize_text(x)
    q_vec = tfidf.transform([x])
    q_pred = classifier.predict_proba(q_vec) #getting probabilities of all labels for given recipe text

    suggested_labels = []
    counter = 0
    for x in binarizer.classes_: #leaving only labels that have probabilities more than 0.75%
        proba = round(q_pred[0][counter], 2)
        if proba > 0.75:
            suggested_labels.append(str(x))
        counter += 1
    prediction = suggested_labels

    prediction = str(prediction).strip('[()]').replace("'", "")

    print('prediction:' + prediction) #print for heroku logs

    prediction = prediction.split(", ")
    response = json.dumps({'response': prediction}, ensure_ascii=False)
    return response, 200 #sending response to frontend


if __name__ == '__main__':
    application.run(debug=True)
