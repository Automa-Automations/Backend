import os
import sys

sys.path.append(os.path.abspath("../../"))

from flask import Flask
from flask_fs_router import FlaskFSRouter

app = Flask(__name__)
FlaskFSRouter(app)

if __name__ == "__main__":
    app.run(debug=True, port=10, host="0.0.0.0")
