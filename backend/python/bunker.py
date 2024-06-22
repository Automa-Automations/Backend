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
import time
import uuid
from pyngrok import ngrok

from colorama import Fore, Style, init
import ast

init(autoreset=True)

def get_top_level_function_names(file_path):
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)

    top_level_function_names = [
        node.name for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.col_offset < 1
    ]

    return top_level_function_names


def get_top_level_class_methods(file_path):
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)

    class_methods = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            for body_item in node.body:
                if isinstance(body_item, ast.FunctionDef):
                    method_name = body_item.name
                    class_methods.append(f"CLASS/{class_name}/{method_name}")

    return class_methods

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
    dockerfile = dockerfile.replace("<<app_run>>", "cd " + os.path.join(root_dir) + "; ")
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

                if "[notice] A new release of pip" in pretty_output:
                    continue

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
    ports_transformed = {str(internal)+"/tcp": str(external) for internal, external in ports.items()}

    mounts_transformed = []
    for mount_name, mount_location in mounts.items():
        mounts_transformed.append(docker.types.Mount(target=mount_location, source=mount_name, type='volume'))

    # CHeck if container is running & cancel it if it is is.
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


def ask_flask_route_config():
    config = {
        "route": questionary.text("What route would you like to create?").ask()
    }

    return config


def flask_route_builder(service, all):
    flask_routes_config = ask_flask_route_config()
    routes = flask_routes_config['route'].split('/')

    if routes[0] != '':
        routes = [''] + routes

    config = json.load(open("config.json"))

    service_path = os.path.join(config['create']['service_dir'], service)

    routes_path = os.path.join(service_path, "pages")
    types_of_routes = ["post", "put", "get", "delete"]


    with yaspin(text=f"⤵️ Building Routes...") as sp:
        for route in routes:
            routes_path = os.path.join(routes_path, route)
            sp.text = f"Building Route {routes_path}"

            if not os.path.exists(routes_path):
                os.mkdir(routes_path)

            if not os.listdir(routes_path):
                files_to_create = [os.path.join(routes_path, f"index({rt}).py") for rt in types_of_routes]

                for file in files_to_create:
                    file_ = open(file, "w")
                    file_.write(f'def default(): return "Hello, {file}"')

def is_service_running(service) -> bool:
    client = docker.from_env()
    try:
        container = client.containers.get(service)
        if not container:
            return False

        container_state = container.attrs["State"]
        return container_state["Status"] == "running" 
    except docker.errors.NotFound:
        return False
     

def ngrok_container(service: str):
    with yaspin(text=f"🚀 Publishing Container via NGROK...") as sp:
        if not is_service_running(service):
            sp.text = "🛑 Service is not running. Starting service..."
            container_runner(service, all=False)
        
        # Get the exposed external port
        sp.text = "🔍 Getting external port..."
        client = docker.from_env()
        container = client.containers.get(service)
        ports = container.attrs["NetworkSettings"]["Ports"]
        external_port = list(ports.keys())[0].split("/")[0]
        
        sp.text = "⇝ Publishing the service..."
        http_tunnel = ngrok.connect(external_port)
        sp.text = f"🎉 Service is live at: {http_tunnel.public_url}"

        click.echo(f" Press '^ + C' to stop the service")

        live_text = sp.text
        try:
            alive_for = 0
            while True:
                alive_for += 0.1
                time.sleep(0.1)
                sp.text = f"{live_text} {alive_for:.2f}s"

        except KeyboardInterrupt:
            sp.stop()
            ngrok.kill()

        click.echo(f"🎉 Service is live at: {http_tunnel.public_url}")
        click.echo('😥 Killed Ngrok Service.')


def test_builder(type_, path, dir_path="", tests_path=""):
    if not dir_path:
        config = json.load(open("config.json"))
        services_dir = config.get('create', {}).get('service_dir', {})

        if not services_dir:
            services_dir = choose_or_make_dir("services", ".", False)

        match type_:
            case "service":
                dir_path = os.path.join(services_dir, path)
                tests_path = os.path.join(dir_path, "BunkerTests")
            case "src":
                dir_path = path
                tests_path = os.path.join(path, "BunkerTests")

        if not os.path.exists(tests_path):
            os.mkdir(tests_path)


    excluded = ["venv", "__pycache__", "__init__.py"]

    # List the root dir
    content = os.listdir(dir_path)

    for item in content:
        if item in excluded:
            continue

        item_path = os.path.join(dir_path, item)
        item_type = "file" if os.path.isfile(item_path) else "dir"
        test_dir = os.path.join(tests_path, item).replace(".py", "")

        # Ensure the filename doesn't have BunkerTest inside of it (Directories included)
        if "BunkerTest" in item_path:
            continue

        if item_type == "dir":
            if not os.path.exists(test_dir):
                os.mkdir(test_dir)

            test_builder(type_=type_, path=path, dir_path=item_path, tests_path=test_dir)

        if item_type == "file" and item_path.split('.')[-1] == "py":
            if not os.path.exists(test_dir):
                os.mkdir(test_dir)

            # Get all the functions
            functions = get_top_level_function_names(item_path)
            class_methods = get_top_level_class_methods(item_path)
            functions += class_methods

            # Create a new file for each function
            for function in functions:
                if function.startswith("CLASS"):
                    segments = function.split("/")

                    if "/CLASS" in test_dir:
                        test_dir = "/".join(test_dir.split("/")[:-1])

                    if not test_dir.endswith("".join(segments[:2])):
                        class_path = os.path.join(test_dir, "".join(segments[:2]))
                        item_path += "class"
                        if not os.path.exists(class_path): os.mkdir(class_path)
                        test_dir = class_path

                    function = segments[-1].replace("__", "")
                    if function == "init": function = function.upper()

                function_path = os.path.join(test_dir, f"{function}.py")

                if os.path.exists(function_path):
                    continue

                with open(function_path, "w") as f:
                    file_base_content = open("templates/UnitTestTemplate.py", "r").read()
                    test_name_ = item_path.replace(".py", "").split("/")
                    test_name_ += [function]
                    test_name = "".join([i.replace("(", "").replace(")", "").capitalize() for i in test_name_])
                    file_base_content = file_base_content.replace("<<test_name>>", test_name)
                    f.write(file_base_content)


@builder.command()
@click.option("--service", "-s", help="The service to run.", required=False, type=str)
@click.option("--new", "-n", help="Start a new service.", required=False, type=str, is_flag=True)
def flask(service, new):
    """Utility to generate flask templates, routes, files & tests"""
    config = json.load(open("config.json"))
    services_dir = config.get('create', {}).get('service_dir', {})
    
    if not services_dir or not os.path.exists(services_dir):
        services_dir = choose_or_make_dir("service", ".")

       
    if new and service:
        services_dir = os.path.join(services_dir, service)
        os.mkdir(services_dir)
        new = True   
        
    if not new and not service and questionary.confirm("Would you like to create a new service?").ask():
        service = questionary.text("Service Name:").ask()
        services_dir = os.path.join(services_dir, service)
        os.mkdir(services_dir)
        new = True
    elif not service:
        service = questionary.select("Choose a service: ", choices=os.listdir(services_dir)).ask()


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
        "Create a new route (Also creates tests)", # Done
        "Create Test cases for Missing Tests", 
        "Build the service", # Done
        "Run the service with Docker", # Done
        "Get public url for testing" # Done
    ]

    # Ask the user what they want to do
    task = questionary.select("What action would you like to take?", choices=flask_tasks).ask()
    if task == "Create a new route (Also creates tests)":
        flask_route_builder(service, all=False)
    elif task == "Create Test cases for Missing Tests":
        test_builder(type_='service', path=service)
    elif task == "Build the service":
        container_builder(service=service, all=False)
    elif task == "Run the service with Docker":
        container_builder(service=service, all=False)
        container_runner(service=service, all=False)
    elif task == "Get public url for testing":
        ngrok_container(service=service)



@builder.command()
@click.option("--service", "-s", help="The service to run.", required=False, type=str)
@click.option("--type", "-t", help="The type of service to run.", required=False, type=str)
def codegen(service, type):
    click.echo("Codegen", service, type)
    click.echo(("Codegen", service, type))


if __name__ == "__main__":
    builder()