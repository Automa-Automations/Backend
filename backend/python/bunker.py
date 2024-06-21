# Bunker is a build, template, configuration and auto testing for unit tests, integration tests & production tests.
# Bunker will allow you to generate templates for projects, allowing you to effectively test every single method of a class, every single module & every single package that you are developoing. bunker will also create a generic template for each service, and also create templates for any service your service depends on, in order to test them with each other "integration tests". bunker will also create a template for the production environment, and will allow you to test your service with the production environment, to ensure that your service is working as expected. bunker will also create a template for the production environment, and will allow you to test your service with the production environment, to ensure that your service is working as expected. bunker will also create a template for the production environment, and will allow you to test your service with the production environment, to ensure that your service is working as expected. bunker also effectively injects code into your project to do monitoring, bunker captures all logs into a single generic database, and also captures errors, uptime, usage & more.


import click
import requests
import questionary
from yaspin import yaspin
import docker
import os
import json
from typing import Any
import re
import uuid

from colorama import Fore, Style, init

init(autoreset=True)


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


def get_exposed_ports(image_name):
    # Split the image name into repository and tag
    if ':' in image_name:
        repository, tag = image_name.split(':')
    else:
        repository, tag = image_name, 'latest'

    # Set the registry URL
    registry_url = 'https://registry-1.docker.io'

    # Get the token for accessing the manifest
    auth_url = f'https://auth.docker.io/token?service=registry.docker.io&scope=repository:{repository}:pull'
    token_response = requests.get(auth_url)
    token = token_response.json()['token']

    # Get the image manifest
    manifest_url = f'{registry_url}/v2/{repository}/manifests/{tag}'
    headers = {'Authorization': f'Bearer {token}'}
    manifest_response = requests.get(manifest_url, headers=headers)
    manifest = manifest_response.json()

    # Get the configuration blob
    config = json.loads(manifest['history'][0]['v1Compatibility'])

    # Extract the exposed ports
    exposed_ports = config.get('config', {}).get('ExposedPorts', {})
    ports = list(exposed_ports.keys())
    ports = [port.split('/')[0] for port in ports]

    return ports

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
        "name": f"{name.lower()}_{uuid.uuid4().hex}",
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
    ports_ = get_exposed_ports(image_to_use)
    ports = {str(port.split("/")[0]): str(port.split("/")[0]) for port in ports_}

    for port in ports_:
        click.echo(f"   🛶 {Fore.YELLOW} Detected port {port}")

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

def choose_or_make_dir(type: str, root_dir: str, make_new=True):
    root_dir_files = os.listdir(root_dir)
    if make_new:
        create_or_choose = questionary.select(
            f"Would you like to create a new {type} directory or choose an existing one?",
            choices=["Create", "Choose"]).ask()
    else:
        create_or_choose = "Choose"

    if create_or_choose == "Choose":
        root_dir = questionary.select("Select a root directory:", choices=root_dir_files).ask()
    else:
        root_dir = questionary.text(f"{type.capitalize()} Directory Name:").ask()
        os.mkdir(root_dir)

    return root_dir


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
        root_dir = choose_or_make_dir("service", ".")
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


def build_container(service, dockerfile_path, path, should_stream_output=False) -> str:
    client = docker.APIClient()
    try:
        stream = client.build(path=path, tag=service.lower(), dockerfile=dockerfile_path, decode=True, )
        spinner = None
        for line in stream:
            if 'stream' in line:
                if "--->" in line['stream']:
                    continue

                if "Successfully tagged" in line['stream']:
                    if spinner:
                        spinner.stop()
                        spinner.ok("✅")
                    return line['stream'].split(" ")[-1].strip().replace("\n", "")

                if not should_stream_output:
                    continue

                if line['stream'].strip() == "":
                    continue

                pretty_output = line['stream'].encode('utf-8').decode('unicode-escape').strip()
                pretty_output = pretty_output.replace(
                    "â", ""
                ).replace(
                    "WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv",
                    ""
                )

                # Remove anything that is not ASCII
                pretty_output = "".join([i if ord(i) < 128 else ' ' for i in pretty_output])

                if len(":".join(pretty_output.split(":")[1:]).strip()) == 0:
                    continue

                if not spinner:
                    spinner = yaspin(text=f"{pretty_output}")
                    spinner.start()

                if "Step" in pretty_output:
                    spinner.stop()
                    spinner.ok("✅")
                    spinner = yaspin(text=f"{pretty_output}")
                    spinner.start()
                else:
                    spinner.text = f"{spinner.text.split(':')[0]}: {pretty_output[:50]}..."

            if 'error' in line:
                if "--->" in line['stream']:
                    continue

                if line['stream'].strip() == "":
                    continue

                click.echo(f"{Fore.RED}Error: {line['error']}", err=True)
                break


    except docker.errors.BuildError as e:
        click.echo(f"{Fore.RED}BuildError: {e}", err=True)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)

    if spinner:
        spinner.ok("✅")
        spinner.stop()

    return ""

def container_builder(service, all):
    services = []
    # Get the services directory
    config = json.load(open("config.json"))
    services_dir = config.get('create', {}).get('service_dir', {})
    if not services_dir:
        services_dir = choose_or_make_dir("services", ".")

    services_in_service_dir = os.listdir(services_dir)

    if all:
        services = os.listdir(services_dir)

    if not service and not all:
        service = questionary.select("Select a service to build:", choices=services_in_service_dir).ask()
        services = [service]
    elif service:
        services = [service]

    for service in services:

        service_path = os.path.join(services_dir, service)

        if not os.path.isdir(service_path):
            continue

        click.echo(f"{Fore.GREEN}Building Docker image for service: {service}")
        dockerfile_path = os.path.join(service_path, "Dockerfile")
        config_path = os.path.join(service_path, "config.json")
        service_name = json.load(open(config_path)).get("name", uuid.uuid4().hex)

        df_exists = os.path.exists(dockerfile_path)
        cf_exists = os.path.exists(config_path)

        if not df_exists and not cf_exists:
            click.echo(f"❌{Fore.RED}Error: Dockerfile and Config does not exist at path {service_path}")
            return

        if df_exists and not cf_exists:
            click.echo(f"❌{Fore.RED}Error: Dockerfile but Config file doesn't exist. Deployment isn't possible!")
            return

        if not df_exists and cf_exists:
            click.echo(f'🎉 {service} is a "Deploy Only" container!')
            continue

        click.echo(
            f'{Fore.GREEN}🎉 Built Image: {build_container(service_name, dockerfile_path, "./", should_stream_output=True)}')


@builder.command()
@click.option("--service", "-s", help="The service to build.", required=False, type=str)
@click.option("--all", "-a", help="Builds every single service at once.", required=False, type=str, is_flag=True)
def build(service, all):
    container_builder(service, all)


def container_runner(service: str, all: bool=False):
    config = json.load(open("config.json"))
    services_dir = config.get('create', {}).get('service_dir', {})

    if not services_dir:
        services_dir = choose_or_make_dir("services", ".", False)
    
    if not service and not all:
        service = questionary.select("Select a service to run:", choices=os.listdir(services_dir)).ask()

    service_path = os.path.join(services_dir, service)
    service_config_path = os.path.join(service_path, "config.json")

    service_config = json.load(open(service_config_path))
    client = docker.from_env()

    ports = service_config.get("ports", {})
    mounts = service_config.get("mounts", {})
    env = service_config.get("env", {})
    base_image = service_config.get("base_image")
    image = service_config.get("name").lower() if not base_image else base_image
    ports_transformed = {str(external): str(internal) for internal, external in ports.items()}

    mounts_transformed = []
    for mount_name, mount_location in mounts.items():
        mounts_transformed.append(docker.types.Mount(target=mount_location, source=mount_name, type='volume'))

    container = client.containers.run(
        image=image,
        name=service,
        ports=ports_transformed,
        mounts=mounts_transformed,
        environment=env,
        detach=True,
    )

    return container

@builder.command()
@click.option("--service", "-s", help="The service to run.", required=False, type=str)
@click.option("--all", "-a", help="Runs every single service at once.", required=False, type=str, is_flag=True)
def run(service, all=False):
    """Allows you to run a service if it exists, """
    container_runner(service=service, all=all)


@builder.command()
@click.option("--service", "-s", help="The service to run.", required=False, type=str)
@click.option("--new", "-n", help="Start a new service.", required=False, type=str, is_flag=True)
def flask(service, new):
    "Utility to generate flask templates, routes, files & tests"
    config = json.load(open("config.json"))
    services_dir = config.get('create', {}).get('service_dir', {})

    if not services_dir:
        services_dir = choose_or_make_dir("service", ".")
       
    if service and os.path.exists(os.path.join(services_dir, service)):
        click.echo(f"Service {service} already exists.")
        return
    
    if new and service:
        services_dir = os.path.join(services_dir, service)
        os.mkdir(services_dir)
        new = True   
        
    if not new and not service and questionary.confirm("Would you like to create a new service?").ask():
        service = questionary.text("Service Name:").ask()
        services_dir = os.path.join(services_dir, service)
        os.mkdir(services_dir)
        new = True

    if new and not service:
        service = questionary.text("Service Name:").ask()
        services_dir = os.path.join(services_dir, service)
        os.mkdir(services_dir)
        new = True

    

    service_files_dir = os.path.join(services_dir, service)
    if new:
        click.echo("Creating new Flask service...")
        flask_quickstart(service, services_dir)
   
    # Now we can figure out what the user wants to do
    flask_tasks = [
        "Create a new route (Also creates tests)",
        "Validate test coverage",
        "Build the service",
        "Run the service with Docker",
        "Get public url for testing"
    ]

    # Ask the user what they want to do
    task = questionary.select("What action would you like to take?", choices=flask_tasks).ask()
    if task == "Create a new route (Also creates tests)":
        print("Creating a new route")
    elif task == "Validate test coverage":
        print("Validating test coverage")
    elif task == "Build the service":
        print("Building the service")
    elif task == "Run the service with Docker":
        container_builder(service=service, all=False)
        container_runner(service=service, all=False)
    elif task == "Get public url for testing":
        print("Getting public url for testing")
    


@builder.command()
@click.option("--service", "-s", help="The service to run.", required=False, type=str)
@click.option("--type", "-t", help="The type of service to run.", required=False, type=str)
def codegen(service, type):
    click.echo("Codegen", service, type)
    click.echo(("Codegen", service, type))


if __name__ == "__main__":
    builder()
