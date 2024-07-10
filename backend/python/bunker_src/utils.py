import json
import os
from typing import Any

import click
import requests
from bunker_src.ui.choose_or_make_dir import choose_or_make_dir
import questionary

config_path = "config.json"

def get_service_dir():
    config = json.load(open(config_path))
    service_dir = config.get("create", {}).get("service_dir", {})

    if not service_dir:
        service_dir = choose_or_make_dir("services", ".")

        save_default = questionary.confirm(
            "Would you like to save this as the default service directory?"
        ).ask()

        if save_default:
            config["create"]["service_dir"] = service_dir
            json.dump(config, open(config_path, "w"), indent=4)

    return service_dir

def global_options(func: Any) -> Any:
    @click.option(
        "--config", type=click.Path(), help="Path to the config file."
    )
    def new_func(config: Any, *args: Any, **kwargs: Any):
        global config_path

        if config and not os.path.exists(config):
            click.echo(
                f"😥 The config path you provide {config} does not exist!"
            )
            exit(1)

            config_path = config
        return func(*args, **kwargs)

    return new_func


def get_exposed_ports(image_name: str):
    # Split the image name into repository and tag
    if ":" in image_name:
        repository, tag = image_name.split(":")
    else:
        repository, tag = image_name, "latest"

    # Set the registry URL
    registry_url = "https://registry-1.docker.io"

    # Get the token for accessing the manifest
    auth_url = f"https://auth.docker.io/token?service=registry.docker.io&scope=repository:{repository}:pull"
    token_response = requests.get(auth_url)
    token = token_response.json()["token"]

    # Get the image manifest
    manifest_url = f"{registry_url}/v2/{repository}/manifests/{tag}"
    headers = {"Authorization": f"Bearer {token}"}
    manifest_response = requests.get(manifest_url, headers=headers)
    manifest = manifest_response.json()

    # Get the configuration blob
    config = json.loads(manifest["history"][0]["v1Compatibility"])

    # Extract the exposed ports
    exposed_ports = config.get("config", {}).get("ExposedPorts", {})
    ports = list(exposed_ports.keys())
    ports = [port.split("/")[0] for port in ports]

    return ports
