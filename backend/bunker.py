# Bunker is a build, template, configuration and auto testing for unit tests, integration tests & production tests.
# Bunker will allow you to generate templates for projects, allowing you to effectively test every single method of a class, every single module & every single package that you are developoing. bunker will also create a generic template for each service, and also create templates for any service your service depends on, in order to test them with each other "integration tests". bunker will also create a template for the production environment, and will allow you to test your service with the production environment, to ensure that your service is working as expected. bunker will also create a template for the production environment, and will allow you to test your service with the production environment, to ensure that your service is working as expected. bunker will also create a template for the production environment, and will allow you to test your service with the production environment, to ensure that your service is working as expected. bunker also effectively injects code into your project to do monitoring, bunker captures all logs into a single generic database, and also captures errors, uptime, usage & more.


import click
import questionary
from yaspin import yaspin
import docker
import os
import webbrowser


def dockerhub_quickstart(name):
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
    dockerhub_url = f"https://hub.docker.com/r/{image_to_use}"
    webbrowser.open(dockerhub_url)
    click.echo(f"🌐 Opening browser to {dockerhub_url}")

    # Create the service
    config = {
        "base_image": image_to_use,
        "name": name,
        "cpu": 0,
        "memory": 0,
        "gpu": "",
        "ports": {},
        "mounts": {},
        "env": [],
    }

    # CPU
    cpu_cores = ["0.25", "0.5", "1", "2", "4", "8", "16", "32"]
    cpu = questionary.select("Select CPU Cores:", choices=cpu_cores).ask()
    config["cpu"] = cpu

    # Memory
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
    gpus = ["auto", "none", "a10", "l40s", "a100-40gb", "a100-80gb"]
    gpu = questionary.select("Select GPU:", choices=gpus).ask()
    config["gpu"] = gpu

    # PORTS (Auto Detectable)
    click.echo("🔍 Detecting ports...")
    # TODO: Find a way to detect ports (By inspecting the image dockerfile)
    ports = {}
    config["ports"] = ports
    
    # Mounts
    mounts = {}
    has_any_mounts = questionary.confirm("Do you have any mounts?").ask()
    if has_any_mounts:
        while True:
            mount_name = questionary.text("Mount Name:").ask()
            mount_path = questionary.text("Mount Path:").ask()
            mounts[mount_name] = mount_path
            add_another = questionary.confirm("Add another mount?").ask()
            if not add_another:
                break

    # Environment Variables
    env_vars = {}
    has_any_env_vars = questionary.confirm("Do you have any environment variables?").ask()
    if has_any_env_vars:
        while True:
            env_var_name = questionary.text("Environment Variable Name:").ask()
            env_var_value = questionary.text("Environment Variable Value:").ask()
            env_vars[env_var_name] = env_var_value
            add_another = questionary.confirm("Add another environment variable?").ask()
            if not add_another:
                break
    

@click.group()
def builder():
    """Bunker's code building CLI."""
    pass


@builder.command()
def create():
    """Create a new service from template. Or from scratch."""
    # Service Name
    name = questionary.text("Service Name:").ask()

    if os.path.exists(name):
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

    os.mkdir(name)

    # Create the service
    should_use_template = questionary.confirm("Would you like to use a template?").ask()
    if should_use_template:
        template = questionary.select("Select a template:", choices=[
            "DockerHub - Non-Modified Dockerhub Image",
            "Web - A simple web service",
        ]).ask()
        if template == "DockerHub - Non-Modified Dockerhub Image":
            dockerhub_quickstart(name)

if __name__ == "__main__":
    builder()
