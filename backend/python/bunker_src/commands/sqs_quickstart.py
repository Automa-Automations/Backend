import json
import os
import uuid


def main(service_name, service_path):
    os.system(f"cp -r templates/SqSTemplate/* {service_path}")

    config_path = os.path.join(service_path, "config.json")
    config = json.load(open(config_path, "r"))
    config["name"] = f"{service_name}_{uuid.uuid4().hex}"

    service_dockerpath = os.path.join(service_path, "Dockerfile")
    dockerfile = open(service_dockerpath, "r").read()
    dockerfile = dockerfile.replace("<<service_dir>>", service_path)

    with open(service_dockerpath, "w") as f:
        f.write(dockerfile)
