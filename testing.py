import ollama
import requests

import src

host = requests.resolve_alias("http://ollama.internal:11434")  # type: ignore
print(host)

client = ollama.Client(host=host)
print(client.generate("llama3", "hi"))
