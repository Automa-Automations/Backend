import os
import sys

sys.path.append(os.path.abspath("../../"))

from flask import Flask, abort, request
from flask_fs_router import FlaskFSRouter

app = Flask(__name__)


def is_valid_api_key(api_key):
    return api_key == os.environ["ADMIN_API_KEY"]


@app.before_request
def check_api_key():
    api_key = request.headers.get("A-API-KEY")
    if not api_key or not is_valid_api_key(api_key):
        abort(401, description="Invalid API Key")


FlaskFSRouter(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
