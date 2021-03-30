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
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

#import sys
#print(sys.path)

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

with open('IBMkey.key', 'r') as file:
    APIkey = file.read().replace('\n', '')  #reading api key for machine translation of texts
with open('IBMurl.key', 'r') as file:
    APIurl = file.read().replace('\n', '')  #reading api key for machine translation of texts


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

classifier = load_classifier()
tfidf = load_tfidf()
binarizer = load_binarizer()


def remove_stopwords(text):
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)

# main endpoint
@app.route('/predict', methods=['POST'])
def predict():
    request_json = request.get_json()
    x = str(request_json['input'])
    print(x)

    authenticator = IAMAuthenticator(APIkey)
    language_translator = LanguageTranslatorV3(
        version='2018-05-01',
        authenticator=authenticator
    )
    language_translator.set_service_url(APIurl)
    translation = language_translator.translate(
        text=x,
        model_id='ru-en').get_result()
    watsonResp = json.loads(json.dumps(translation))['translations'][0]['translation']

    recipe_text = str(watsonResp)
    print(recipe_text)
    recipe_text = re.sub(",", "", recipe_text)
    recipe_text = clean_text(recipe_text)
    recipe_text = remove_stopwords(recipe_text)
    recipe_text = lemmatize_text(recipe_text)
    q_vec = tfidf.transform([recipe_text])
    q_pred = classifier.predict_proba(q_vec) #getting probabilities of all labels for given recipe text

    suggested_labels = []
    class_num = 0
    for x in binarizer.classes_: #leaving only labels that have probabilities more than 0.75%
        proba = q_pred[0][class_num]
        if proba > 0.75:
            suggested_labels.append(str(x))
        class_num += 1
    prediction = suggested_labels

    prediction = str(prediction).strip('[()]').replace("'", "")

    print('prediction:' + prediction) #print for heroku logs

    prediction = prediction.split(", ")
    response = json.dumps({'response': prediction}, ensure_ascii=False)
    return response, 200 #sending response to frontend


if __name__ == '__main__':
    application.run(debug=True)
