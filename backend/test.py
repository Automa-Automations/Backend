import requests
import uuid
import json

headers = {"Content-Type": "application/json",
        "Authorization": ""
   }


def create_app():
    url = "https://api.machines.dev/v1/apps"

    payload = {
        "app_name": uuid.uuid4().hex,
        "enable_subdomains": True,
        "network": "",
        "org_slug": "personal"
    }
    response = requests.post(url, json=payload, headers=headers)

    print(response.json())
    return response.json()['id'], payload['app_name']

def create_machine(app_id, app_name):
    import requests

    url = f"https://api.machines.dev/v1/apps/{app_name}/machines"

    payload = { "config": {
      "init": {
        "exec": [
        ]
      },
      "image": "ollama/ollama",
      "auto_destroy": True,
      "restart": {
        "policy": "always"
      },
    "mounts": [{
        "source": "ollama",
        "destination": "/root/.ollama",
    }],
    "services": [
          {
            "ports": [
                {
                "port": 11434,
                "handlers": [
                  "http"
                ]
              }
            ],
            "protocol": "tcp",
            "internal_port": 11434 
          }
        ],
      "guest": {
        "cpu_kind": "shared",
        "cpus": 1,
        "memory_mb": 512
      }
    }
   }

    response = requests.post(url, json=payload, headers=headers)

    print(json.dumps(response.json(), indent=4))

create_machine(*create_app())
