# -*- coding: utf-8 -*-
import flask
from flask import Flask, jsonify, request
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
app.config['JSON_AS_ASCII'] = False

def load_models():
    file_name = "models/finalized_model.sav"
    loaded_model = pickle.load(open('models/finalized_model.sav', 'rb'))
    return loaded_model

def clean_text(text):
    text = re.sub("\'", "", text)
    text = re.sub("[^а-яА-ЯЁё]"," ",text)
    text = ' '.join(text.split())
    text = text.lower()
    return text

nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))
def remove_stopwords(text):
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)

@app.route('/predict', methods=['GET'])

def predict():

    # parse input features from request
    # todo:
    request_json = request.get_json()
    x = str(request_json['input'])
    print(x)
    #x = 'борщ'
    loaded_model = load_models()
    x = clean_text(x)
    x = remove_stopwords(x)
    tfidf_loaded = pickle.load(open('models/tfidf.pickle', 'rb'))
    q_vec = tfidf_loaded.transform([x])
    prediction = loaded_model.predict(q_vec)[0]
    print(prediction)
    #prediction = prediction.encode('utf8')
    print(prediction.encode('utf-8'))
    response = json.dumps({'response': prediction}, ensure_ascii=False)
    #todo encoding
    return response, 200

if __name__ == '__main__':
    application.run(debug=True)
