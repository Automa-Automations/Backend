import json
import os
import uuid

from bunker_src.ui.ask_config import ask_config_json_questions


def main(service_name, service_path):
    os.system(f"cp -r templates/SqSTemplate/* {service_path}")

    config_path = os.path.join(service_path, "config.json")
    config = json.load(open(config_path, "r"))
    config["name"] = f"{service_name}_{uuid.uuid4().hex}"

    ask_config_json_questions(config)

    json.dump(config, open(config_path, "w"), indent=4)

    # Modify the Dockerfile
    service_dockerpath = os.path.join(service_path, "Dockerfile")
    dockerfile = open(service_dockerpath, "r").read()
    dockerfile = dockerfile.replace("<<service_dir>>", service_path)

    with open(service_dockerpath, "w") as f:
        f.write(dockerfile)
