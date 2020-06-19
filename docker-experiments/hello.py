from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    print('log: new request!!!')
    return 'Hello, world!'