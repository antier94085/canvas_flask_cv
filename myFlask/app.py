from flask import Flask
from flask_cors import CORS

from appRoutes import register 

app = Flask(__name__)

register(app)

CORS(app)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run( debug=False, host='127.0.0.1', port=5050)