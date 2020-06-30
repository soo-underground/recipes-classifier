from flask import Flask
from flask.logging import create_logger
import numpy as np
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from joblib import dump, load

app = Flask(__name__)
LOG = create_logger(app)

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

    knn = load('knn.pkl')

    param = np.array(param).reshape(1,-1)
    predict = knn.predict(param)

    return str(predict)