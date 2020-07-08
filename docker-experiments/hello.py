from flask import Flask, request, jsonify, abort, redirect, url_for, render_template
from flask.logging import create_logger
import numpy as np
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from joblib import dump, load
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import os



app = Flask(__name__)
LOG = create_logger(app)
knn = load('knn.pkl')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def hello_world():
    print('log: new request!!!')
    return 'Hello, world!!!'

@app.route('/name/<myname>')
def hello_name(myname):
    LOG.info('log: new request from %s' % myname)
    return 'Hello, %s!!!' % myname

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

@app.route('/avg/<nums>/')
def avg(nums):
    nums = nums.split(',')
    nums = [float(num) for num in nums]
    nums_mean = mean(nums)
    return 'average is %s!!!' % str(nums_mean)

@app.route('/iris/<param>')
def iris(param):

    param = param.split(',')
    param = [float(param) for param in param]

    param = np.array(param).reshape(1,-1)
    predict = knn.predict(param)
    print(str(predict))

    return str(predict)

@app.route('/show_image')
def show_image():
    return '<img src="static/cook.jpg" alt="cooking2">'

@app.route('/iris_post', methods=['POST'])
def iris_post():

    try:
        content = request.get_json()

        param = content['flower'].split(',')
        param = [float(param) for param in param]

        param = np.array(param).reshape(1,-1)
        predict = knn.predict(param)

        predict = {'class':str(predict[0])}
    except:
        return redirect(url_for('bad_request'))

    return jsonify(predict)

@app.route('/badrequest400')
def bad_request():
    return abort(400) 

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    
@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        print(str(form.name))
        return ('nice')
    return render_template('submit.html', form=form)

@app.route('/success', methods=['GET', 'POST'])
def success():
    return ('nice')