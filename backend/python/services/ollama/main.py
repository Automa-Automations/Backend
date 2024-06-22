import os
import sys
sys.path.append(os.path.abspath('../../'))

from flask import Flask
from flask_fs_router import FlaskFSRouter

app = Flask(__name__)
FlaskFSRouter(app)

class Hi():
    def __init__(self):
        print("THIS IS SOME RANDOM THING")

    def hi(self):
        print("SAY HI")

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
