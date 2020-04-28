# -*- coding: utf-8 -*-
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

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

def load_classifier():
    classifier = pickle.load(open('models/multilabel_model.sav', 'rb'))
    return classifier

def load_tfidf():
    tfidf = pickle.load(open('models/tfidf.sav', 'rb'))
    return tfidf

def load_binarizer():
    binarizer = pickle.load(open('models/multilabel_binarizer.sav', 'rb'))
    return binarizer

def clean_text(text):
    text = re.sub("\'", "", text)
    text = re.sub("[^а-яА-ЯЁё]"," ",text)
    text = ' '.join(text.split())
    text = text.lower()
    return text

from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
def lemmatize_text(text):
    lemmatized_text=[]
    sentence_words = nltk.word_tokenize(text)
    for word in sentence_words:
        lemmatized_text.append(wordnet_lemmatizer.lemmatize(word, pos="v"))
    lemmatized_text = ' '.join(lemmatized_text)
    return lemmatized_text

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
def remove_stopwords(text):
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)

@app.route('/predict', methods=['POST'])

def predict():

    # parse input features from request
    # todo:
    request_json = request.get_json()
    x = str(request_json['input'])
    print(x)
    #x = 'борщ'
    classifier = load_classifier()
    tfidf = load_tfidf()
    binarizer = load_binarizer()

    x = clean_text(x)
    x = remove_stopwords(x)
    x = lemmatize_text(x)
    tfidf_loaded = pickle.load(open('models/tfidf.pickle', 'rb'))
    q_vec = load_tfidf().transform([x])
    prediction = load_classifier().predict(q_vec)
    prediction = load_binarizer().inverse_transform(prediction)
    print(prediction)
    prediction = str(prediction).strip('[()]')
    print(prediction)
    #prediction = ' '.join(prediction)
    #print(prediction)
    #prediction = prediction.encode('utf8')
    print(prediction.encode('utf-8'))
    response = json.dumps({'response': prediction}, ensure_ascii=False)
    #todo encoding
    return response, 200

if __name__ == '__main__':
    application.run(debug=True)
