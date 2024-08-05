import requests

import src

print(requests.get("http://imageapi.internal:5000").text)
