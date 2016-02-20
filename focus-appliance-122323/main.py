from flask import Flask
from fhired.tests import testing
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/tests')
def tests():
    output = testing()
    return "<br/>".join(output)

if __name__ == '__main__':
    app.run()
