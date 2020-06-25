from flask import Flask
from flask.logging import create_logger
import numpy as np
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier

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

    LOG.info(param)

    iris = datasets.load_iris()
    iris_X = iris.data 
    iris_y = iris.target 

    np.random.seed(0)
    indices = np.random.permutation(len(iris_X))
    iris_X_train = iris_X[indices[:-10]] 
    iris_y_train = iris_y[indices[:-10]] 
    iris_X_test = iris_X[indices[-10:]] 
    iris_y_test = iris_y[indices[-10:]]

    knn = KNeighborsClassifier()
    knn.fit(iris_X_train, iris_y_train) 
    KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
                         metric_params=None, n_jobs=1, n_neighbors=5, p=2,
                         weights='uniform'
                         )
    knn.predict(iris_X_test)

    param = np.array(param).reshape(1,-1)
    predict = knn.predict(param)

    return str(predict)