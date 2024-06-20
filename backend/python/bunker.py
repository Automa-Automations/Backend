# Bunker is a build, template, configuration and auto testing for unit tests, integration tests & production tests.
# Bunker will allow you to generate templates for projects, allowing you to effectively test every single method of a class, every single module & every single package that you are developoing. bunker will also create a generic template for each service, and also create templates for any service your service depends on, in order to test them with each other "integration tests". bunker will also create a template for the production environment, and will allow you to test your service with the production environment, to ensure that your service is working as expected. bunker will also create a template for the production environment, and will allow you to test your service with the production environment, to ensure that your service is working as expected. bunker will also create a template for the production environment, and will allow you to test your service with the production environment, to ensure that your service is working as expected. bunker also effectively injects code into your project to do monitoring, bunker captures all logs into a single generic database, and also captures errors, uptime, usage & more.


import click
import questionary
from yaspin import yaspin
import docker
import os
import json
from typing import Any


def ask_config_json_questions(config: dict[str, Any]):
    config = config.copy()

    # CPU
    cpu_cores = ["0.25", "0.5", "1", "2", "4", "8", "16", "32"]
    cpu = questionary.select("Select CPU Cores:", choices=cpu_cores).ask()
    config["cpu"] = cpu

    # Memory
    # If there is already memory specified in config then ask the user if they want to change it
    should_ask_memory = True
    if config["memory"] and not questionary.confirm(f"Would you like to change the memory? ({config['memory']})").ask():
        should_ask_memory = False

    if should_ask_memory:
        memory_units = ["MB", "GB"]
        memory_unit = questionary.select("Select Memory Unit:", choices=memory_units).ask()

        memory_amounts_mb = ["128", "256", "512", "1024", "2048", "4096", "8192", "16384", "32768", "65536"]
        memory_amounts_gb = ["1", "2", "4", "8", "16", "32", "64"]
        if memory_unit == "MB":
            memory = questionary.select("Select Memory Amount (MB):", choices=memory_amounts_mb).ask()
        else:
            memory = questionary.select("Select Memory Amount (GB):", choices=memory_amounts_gb).ask()

        config["memory"] = f"{memory}{memory_unit}"

    # GPU
    should_ask_gpu = True
    if config["gpu"] and not questionary.confirm(f"Would you like to change the GPU? ({config['gpu']})").ask():
        should_ask_gpu = False

    if should_ask_gpu:
        gpus = ["auto", "none", "a10", "l40s", "a100-40gb", "a100-80gb"]
        gpu = questionary.select("Select GPU:", choices=gpus).ask()
        config["gpu"] = gpu

    mounts = config.get("mounts", {})
    should_ask_mounts = True
    if mounts and not questionary.confirm("Would you like to change the mounts?").ask():
        should_ask_mounts = False

    if should_ask_mounts:
        should_ask_mounts = questionary.confirm("Would you like to add mounts?").ask()

    if should_ask_mounts:
        while True:
            mount_name = questionary.text("Mount Name:").ask()
            mount_path = questionary.text("Mount Path:").ask()
            mounts[mount_name] = mount_path
            add_another = questionary.confirm("Add another mount?").ask()
            if not add_another:
                break

    config["mounts"] = mounts

    # Environment Variables
    env_vars = config.get("env", {}).copy()
    should_ask_env_vars = True
    if env_vars and not questionary.confirm("Would you like to change the environment variables?").ask():
        should_ask_env_vars = False

    if should_ask_env_vars:
        should_ask_env_vars = questionary.confirm("Would you like to add environment variables?").ask()

    if should_ask_env_vars:
        while True:
            env_var_name = questionary.text("Environment Variable Name:").ask()
            env_var_value = questionary.text("Environment Variable Value:").ask()
            env_vars[env_var_name] = env_var_value
            add_another = questionary.confirm("Add another environment variable?").ask()
            if not add_another:
                break

    config["env"] = env_vars
    return config


def dockerhub_quickstart(name: str, root_dir: str):
    client = docker.from_env()
    image = questionary.text("Docker Image:").ask()

    if not image:
        click.echo("Docker image cannot be empty.")
        return

    with yaspin(text=f"🔍 Searching for {image}") as sp:
        response = client.images.search(image)
        if not response:
            sp.fail("No image found.")
            return
        else:
            sp.text = f"✅ Found {len(response)} images for {image}"
            sp.start()

        image_to_use = questionary.select("Select an image:", choices=[f'{x["name"]}' for x in response]).ask()
        if not image_to_use:
            click.echo("No image selected.")
            return

    click.echo(f"🚀 Creating {name} service from {image_to_use}")

    # Create the service
    config = {
        "base_image": image_to_use,
        "name": name,
        "cpu": 0,
        "memory": 0,
        "gpu": "",
        "ports": {},
        "mounts": {},
        "env": {},
    }
    # Save the config
    click.echo("📝 Saving configuration...")

    # PORTS (Auto Detectable)
    click.echo("🔍 Detecting ports...")
    # TODO: Find a way to detect ports (By inspecting the image dockerfile)
    ports: dict[str, str] = {}
    config["ports"] = ports

    config = ask_config_json_questions(config)

    click.echo("📝 Saving configuration...")
    json.dump(config, open(os.path.join(root_dir, "config.json"), "w"), indent=4)


def flask_quickstart(name, root_dir):
    os.system(f"cp -r templates/Flask/* {root_dir}")
    config = {
        "base_image": None,
        "name": name,
        "cpu": 0,
        "memory": 0,
        "gpu": "",
        "ports": {
            "5000": "80"
        },
        "mounts": {},
        "env": {},
    }

    config = ask_config_json_questions(config)
    click.echo("📝 Saving configuration...")
    json.dump(config, open(os.path.join(root_dir, "config.json"), "w"), indent=4)

    dockerfile_path = os.path.join(root_dir, "Dockerfile")
    if not os.path.exists(dockerfile_path):
        click.echo("Dockerfile not found. Using default Dockerfile.")
        os.system(f"cp templates/Flask/Dockerfile {dockerfile_path}")

    click.echo("📝 Modifying Dockerfile...")
    dockerfile = open(dockerfile_path).read()
    dockerfile = dockerfile.replace("<<port>>", list(config["ports"].keys())[0])
    dockerfile = dockerfile.replace("<<app_name>>", os.path.join(root_dir, "main.py"))
    open(dockerfile_path, "w").write(dockerfile)

    click.echo("📝 Modifying main.py...")
    main_path = os.path.join(root_dir, "main.py")
    main = open(main_path).read()
    main = main.replace("<<port>>", list(config["ports"].keys())[0])
    open(main_path, "w").write(main)

    click.echo("🚀 Flask service created.")


@click.group()
def builder():
    """Bunker's code building CLI."""
    pass


@builder.command()
def create():
    """Create a new service from template. Or from scratch."""
    config = json.load(open("config.json"))
    create_config = config['create']

    # Service Name
    name = questionary.text("Service Name:").ask()
    paths = os.listdir()
    dirs = [x for x in paths if os.path.isdir(x)]

    # Ask which will be the root directory
    if not create_config['service_dir']:
        # Ask them if they want to create or choose a root directory
        create_or_choose = questionary.select(
            "Would you like to create a new root directory or choose an existing one?",
            choices=["Create", "Choose"]).ask()

        root_dir = None
        if create_or_choose == "Choose":
            root_dir = questionary.select("Select a root directory:", choices=dirs).ask()
        else:
            root_dir = questionary.text("Root Directory Name:").ask()
            os.mkdir(root_dir)

        save_default = questionary.confirm("Would you like to save this as the default root directory?").ask()
        if save_default:
            create_config['service_dir'] = root_dir
            json.dump(config, open("config.json", "w"), indent=4)
    else:
        root_dir = create_config['service_dir']
        click.echo(f"⇝ Using root directory: {root_dir}")
        if not os.path.exists(root_dir):
            os.mkdir(root_dir)

    service_path = os.path.join(root_dir, name)
    if os.path.exists(service_path) and len(os.listdir(service_path)) > 0:
        click.echo("Service already exists.")
        return

    # Ensure name doesn't contain special characters
    if not name.isalnum():
        click.echo("Service name can only contain letters and numbers.")
        return

    # Ensure it is not empty
    if not name:
        click.echo("Service name cannot be empty.")
        return

    try:
        os.mkdir(service_path)
    except Exception as e:
        ...

    # Create the service
    should_use_template = questionary.confirm("Would you like to use a template?").ask()
    if should_use_template:
        template = questionary.select("Select a template:", choices=[
            "DockerHub - Non-Modified Dockerhub Image",
            "Flask - An Http Restful API",
            "Cron - A Cron Job Service (Useful for mass data cleaning / processing)",
        ]).ask()
        if template == "DockerHub - Non-Modified Dockerhub Image":
            dockerhub_quickstart(name, service_path)
        if template == "Flask - An Http Restful API":
            flask_quickstart(name, service_path)

@builder.command()
# Add a command to ask which service to build, it isn't nesseary, because we will show them a dropdown, but it is good to have for faster building & non-interactive shells.
@click.option("--service", "-s", help="The service to build.", required=False, type=str)
def build(service):
    print(service)

if __name__ == "__main__":
    builder()
