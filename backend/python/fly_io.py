import requests

headers = {
    "Authorization": "Bearer "
}


def list_apps():
    url = "https://api.machines.dev/v1/apps"

    querystring = {"org_slug":"personal"}

    response = requests.get(url, params=querystring, headers=headers)

    return response.json()['apps']


def does_app_exist(name):
    apps = list_apps()
    return True if len([app for app in apps if app["name"] == name]) > 0 else False


def create_app(name):
    if does_app_exist(name):
        print(f"App {name} already exists")
        return

    url = "https://api.machines.dev/v1/apps"

    payload = {
        "app_name": name,
        "enable_subdomains": True,
        "network": "tcp",
        "org_slug": "personal"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    return response.json()



app_name = "8cbfd719-6c70-48b7-9be0-7bc0ae7cb227"
create_app(app_name)
