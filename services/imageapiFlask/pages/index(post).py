from flask import jsonify


def default():
    return (
        jsonify({"error": "Can't make a POST request to '/' There is nothing here!"}),
        400,
    )
