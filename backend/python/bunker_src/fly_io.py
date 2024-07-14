import json
import os

import click
import requests

headers = {"Authorization": "Bearer fo1_EsFlhIwDIHpJX-ZJbInB6S82rbaIhAgY5TM3O93PwHQ"}


def list_apps():
    url = "https://api.machines.dev/v1/apps"

    querystring = {"org_slug": "personal"}

    response = requests.get(url, params=querystring, headers=headers)

    return response.json()["apps"]


def does_app_exist(name):
    apps = list_apps()
    return (
        True if len([app for app in apps if app["name"] == name.lower()]) > 0 else False
    )


def create_app(name):
    if does_app_exist(name):
        print(f"App {name} already exists")
        return

    url = "https://api.machines.dev/v1/apps"

    payload = {
        "app_name": name.lower(),
        "enable_subdomains": True,
        "network": "tcp",
        "org_slug": "personal",
    }

    response = requests.post(url, json=payload, headers=headers)


def list_machine(app_name):
    url = f"https://api.machines.dev/v1/apps/{app_name}/machines"

    response = requests.get(url, headers=headers)
    response_json = response.json()

    machine_ids = [machine["id"] for machine in response_json]

    return machine_ids


def does_machine_exist(app_name, machine_id):
    machines = list_machine(app_name)
    return True if machine_id in machines else False


def delete_machine(app_name, machine_id):
    if does_machine_exist(app_name, machine_id):
        url = f"https://api.machines.dev/v1/apps/{app_name}/machines/{machine_id}"
        response = requests.delete(url, headers=headers)
        print(response.json())


def list_app_volumes(app_name):
    url = f"https://api.machines.dev/v1/apps/{app_name}/volumes"
    response = requests.get(url, headers=headers)
    response_json = response.json()
    volume_ids = [
        {"id": volume["id"], "name": volume["name"]} for volume in response_json
    ]
    return volume_ids


def create_app_volume(app_name, volume_name, size):
    url = f"https://api.machines.dev/v1/apps/{app_name}/volumes"
    payload = {
        "name": volume_name,
        "size_gb": size,
        "region": "jnb",  # Make the user be able to choose the region, as well as multi region deployments
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()["id"]


def get_mounts(config, app_name):
    mounts = []
    existing_volumes = list_app_volumes(app_name)
    for mount_name, mount_path in config.get("mounts", {}).items():
        if mount_name in [volume["name"] for volume in existing_volumes]:
            volume_id = [
                volume["id"]
                for volume in existing_volumes
                if volume["name"] == mount_name
            ][0]
        else:
            click.echo(f"Volume {mount_name} does not exist. Creating volume...")
            size: int = int(mount_path.split(":")[1])
            volume_id = create_app_volume(app_name, mount_name, size or 10)

        mounts.append(
            {
                "volume": volume_id,
                "path": mount_path.split(":")[0],
            }
        )

    return mounts


def get_fly_services(config):
    services = []
    for internal, external in config.get("ports", {}).items():
        services.append(
            {
                "ports": [
                    {"port": int(external), "handlers": ["tls", "http"]},
                ],
                "protocol": "tcp",
                "autostop": config.get("auto_stop", True),
                "autostart": True,
                "min_machines_running": 0,
                "internal_port": int(internal),
            }
        )
    return services


def create_machine(app_name, image_name, service_config):
    config = service_config
    app_name = app_name.lower()
    url = f"https://api.machines.dev/v1/apps/{app_name}/machines"

    image = image_name

    mounts = get_mounts(config, app_name)
    ports = get_fly_services(config)

    memory_str = config["memory"].lower()
    memory = 256
    if memory_str.endswith("gb"):
        memory = int(memory_str.replace("gb", "")) * 1024
    elif memory_str.endswith("mb"):
        memory = int(memory_str.replace("mb", ""))

    for region in config.get("regions", ["jnb"]):
        payload = {
            "config": {
                "region": region,  # Make the user be able to choose the region, as well as multi region deployments
                "init": {},
                "image": image,
                "auto_destroy": True,
                "restart": {"policy": "always"},
                "mounts": mounts,
                "services": ports,
                "guest": {
                    "cpu_kind": config.get("cpu_mode", "shared"),
                    "cpus": int(config.get("cpu", 1)),
                    "memory_mb": memory,
                },
            }
        }

        if "gpu" in config:
            payload["config"]["guest"]["gpus"] = 1
            payload["config"]["guest"]["gpu_kind"] = (
                config.get("gpu") or "a100-pcie-40gb"
            )

        if schedule := config.get("schedule"):
            payload["config"]["schedule"] = schedule

        response = requests.post(url, json=payload, headers=headers)

        print(response.json())
        return response.json()


def create_machines(app_name, image_name, app_config):
    if not does_app_exist(app_name):
        print(f"App {app_name} does not exist")
        return

    # Delete all machines
    # Create new machines based on regions etc...
    for machine in list_machine(app_name):
        delete_machine(app_name, machine)

    # Create a new machine
    create_machine(app_name, image_name, app_config)


def deploy_image(image_name, service_dir):
    # Create Fly App if not exists

    config_path = os.path.join(service_dir, "config.json")
    app_config = json.load(open(config_path))
    app_name = app_config["name"]
    app_exists = does_app_exist(app_name.lower())
    image_name = (
        image_name if not app_config["base_image"] else app_config["base_image"]
    )

    if "/" not in image_name:
        repository = f"{os.environ['DOCKERHUB_USERNAME']}/{image_name}"
    else:
        repository = image_name

    if not app_exists:
        create_app(app_name.lower())

    create_machines(app_name.lower(), repository, app_config)
