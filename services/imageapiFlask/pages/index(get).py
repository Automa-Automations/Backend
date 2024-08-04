from flask import jsonify


def default():
    return (
        jsonify({"error": "Can't make a GET request to '/' There is nothing here!"}),
        400,
    )
