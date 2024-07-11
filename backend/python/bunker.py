# Bunker is a build, template, configuration and auto testing for unit tests, integration tests & production tests.
# Bunker will allow you to generate templates for projects, allowing you to effectively test every single method of a class, every single module & every single package that you are developoing. bunker will also create a generic template for each service, and also create templates for any service your service depends on, in order to test them with each other "integration tests". bunker will also create a template for the production environment, and will allow you to test your service with the production environment, to ensure that your service is working as expected. bunker will also create a template for the production environment, and will allow you to test your service with the production environment, to ensure that your service is working as expected. bunker will also create a template for the production environment, and will allow you to test your service with the production environment, to ensure that your service is working as expected. bunker also effectively injects code into your project to do monitoring, bunker captures all logs into a single generic database, and also captures errors, uptime, usage & more.
import json
import os

import click
import dotenv
import questionary
from bunker_src.commands.bootstrap import command as bootstrap_command
from bunker_src.cron import cron_quickstart, cron_runner
from bunker_src.docker import (
    build_container,
    container_builder,
    container_runner,
    dockerhub_quickstart,
    push_image,
)
from bunker_src.flask import flask_quickstart, flask_route_builder
from bunker_src.fly_io import deploy_image
from bunker_src.ngrok import ngrok_container
from bunker_src.testing import test_builder, test_runner
from bunker_src.ui.choose_service import choose_service
from bunker_src.utils import config_path, get_service_dir, global_options
from colorama import init

init(autoreset=True)
dotenv.load_dotenv(".bunker.env")


if not os.path.exists(".bunker.env"):
    click.echo(
        "Sorry, But it doesn't seem that you have your environment variables configured!"
    )
    with open(".bunker.env", "w") as f:
        f.write(
            """
DOCKERHUB_USERNAME=""
DOCKERHUB_PASSWORD=""
FLY_IO_API_KEY=""
        """
        )
    exit(1)


@click.group()
@global_options
def builder():
    """Bunker's code building CLI."""
    pass


@builder.command()
def create():
    """Create a new service from template. Or from scratch."""
    # Service Name
    name = questionary.text("Service Name:").ask()

    root_dir = get_service_dir()
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

    # Create the service
    should_use_template = questionary.confirm("Would you like to use a template?").ask()
    if should_use_template:
        template = questionary.select(
            "Select a template:",
            choices=[
                "DockerHub - Non-Modified Dockerhub Image",
                "Flask - An Http Restful API",
                "Cron - A Cron Job Service (Useful for mass data cleaning / processing)",
            ],
        ).ask()
        if template == "DockerHub - Non-Modified Dockerhub Image":
            os.mkdir(service_path)
            dockerhub_quickstart(name, service_path)
        if template == "Flask - An Http Restful API":
            os.mkdir(service_path + "Flask")
            flask_quickstart(name, service_path + "Flask")
        if (
            template
            == "Cron - A Cron Job Service (Useful for mass data cleaning / processing)"
        ):
            os.mkdir(service_path + "Cron")
            cron_quickstart(name, service_path + "Cron")
    else:
        os.mkdir(service_path)
        os.system(f"cp -r templates/BlankTemplate/* {service_path}")
        file = json.load(open(os.path.join(service_path, "config.json")))
        file["name"] = name
        json.dump(
            file,
            open(os.path.join(service_path, "config.json"), "w"),
            indent=4,
        )


@builder.command()
@click.option("--service", "-s", help="The service to build.", required=False, type=str)
@click.option(
    "--all",
    "-a",
    help="Builds every single service at once.",
    required=False,
    type=str,
    is_flag=True,
)
def build(service, all):
    """
    Builds a service from a Dockerfile.
    """
    if not service and not all:
        service = choose_service()

    container_builder(service, all)


@builder.command()
@click.option("--service", "-s", help="The service to run.", required=True, type=str)
@click.option(
    "--rebuild",
    "-r",
    help="Rebuilds the service before running",
    required=False,
    is_flag=True,
)
def run(service, rebuild):
    """Allows you to run a service if it exists,"""
    container_runner(service=service, rebuild=rebuild)


@builder.command()
@click.option("--service", "-s", help="The service to run.", required=False, type=str)
@click.option(
    "--route",
    "-r",
    help="The route path you want to create",
    required=False,
    type=str,
)
@click.option(
    "--test",
    "-test",
    help="The specific test to run",
    required=False,
    type=str,
)
@click.option("--new", "-n", help="Start a new service.", required=False, is_flag=True)
@click.option(
    "--type",
    "-t",
    help="Action name to avoid the interactive shell",
    required=False,
    type=str,
)
def flask(service, new, test, type, route):
    """Utility to generate flask templates, routes, files & tests"""
    services_dir = get_service_dir()

    if service and not service.endswith("Flask"):
        click.echo("💔 You can't use the flask command to run non flask services!")
        exit(1)

    if not test or not type:
        if new and service:
            services_dir = os.path.join(services_dir, service)
            os.mkdir(services_dir)
            new = True

        if (
            not new
            and not service
            and questionary.confirm("Would you like to create a new service?").ask()
        ):
            service = questionary.text("Service Name:").ask()
            services_dir = os.path.join(services_dir, service)
            os.mkdir(services_dir)
            new = True
        elif not new and not service:
            service = questionary.select(
                "Choose a service: ",
                choices=os.listdir([i for i in services_dir if i.endswith("Flask")]),
            ).ask()
        elif new and not service:
            service = questionary.text("Service Name:").ask() + "Flask"

        if new and service:
            services_dir = os.path.join(services_dir, service)
            os.mkdir(services_dir)
            new = True

        service_files_dir = os.path.join(services_dir, service)
        if new:
            click.echo("Creating new Flask service...")
            flask_quickstart(service, services_dir)

    # Now we can figure out what the user wants to do
    flask_tasks = [
        "(route) Create a new route (Also creates tests)",  # Done
        "(test-create) Create Test cases for Missing Tests",  # Done
        "(test) Run Specific Test Cases",  # Done
        "(build) Build the service",  # Done
        "(run) Run the service with Docker",  # Done
        "(ngrok) Get public url for testing",  # Done
    ]

    task = None
    if not test and not type and not route:
        task = questionary.select(
            "What action would you like to take?", choices=flask_tasks
        ).ask()
        task = task.split(" ")[0].replace("(", "").replace(")", "")
    elif type:
        task = type

    if not service.endswith("Flask"):
        click.echo("💔 You can't use the flask command to run non flask services!")
        exit(1)

    if task == "route" or route:
        flask_route_builder(service, all=False, route=route)
        test_builder(type_="service", path=service)
    elif task == "test-create":
        test_builder(type_="service", path=service)
    elif task == "build":
        container_builder(service=service, all=False)
    elif task == "run":
        container_builder(service=service, all=False)
        container_runner(service=service)
    elif task == "ngrok":
        ngrok_container(service=service)
    elif task == "test" or test:
        test_runner(service, all=True, test_path=test)


@builder.command()
@click.option(
    "--test",
    "-test",
    help="The specific test to run",
    required=False,
    type=str,
)
@click.option("--service", "-s", help="The service to run.", required=False, type=str)
@click.option(
    "--new",
    "-test",
    help="Create a new Set of tests.",
    required=False,
    is_flag=True,
)
@click.option(
    "--all",
    "-a",
    help="Runs all tests for a service (Used only with --service)",
    required=False,
    is_flag=True,
)
def test(test, new, service, all):
    """
    Allows you to generate tests, run them and build them.
    """
    if service and new:
        test_builder(type_="service", path=service)

    if new:
        test_builder(type_="src", path=test)

    test_runner(service, test_path=test, all=all)


@builder.command()
@click.option("--service", "-s", help="The service to run.", required=False, type=str)
@click.option(
    "--test",
    "-test",
    help="The specific test to run",
    required=False,
    type=str,
)
@click.option("--new", "-n", help="Start a new service.", required=False, is_flag=True)
@click.option(
    "--all",
    "-a",
    help="Command Specific to the --type",
    required=False,
    is_flag=True,
)
@click.option(
    "--type",
    "-t",
    help="Action name to avoid the interactive shell",
    required=False,
    type=str,
)
def cron(service, test, new, type, all):
    """
    Allows you to generate cron services, run them, test them and build them.
    """
    services_dir = get_service_dir()

    if service and not service.endswith("Cron"):
        click.echo("💔 You can't use the cron command to run non cron services!")
        exit(1)

    if not test or not type:
        if new and service:
            services_dir = os.path.join(services_dir, service)
            os.mkdir(services_dir)
            new = True

        if (
            not new
            and not service
            and questionary.confirm("Would you like to create a new service?").ask()
        ):
            service = questionary.text("Service Name:").ask()
            services_dir = os.path.join(services_dir, service)
            os.mkdir(services_dir)
            new = True
        elif not service:
            service = questionary.select(
                "Choose a service: ",
                choices=[i for i in os.listdir(services_dir) if i.endswith("Cron")],
            ).ask()
        elif not new and not service:
            service = questionary.select(
                "Choose a service: ",
                choices=os.listdir([i for i in services_dir if i.endswith("Flask")]),
            ).ask()
        elif new and not service:
            service = questionary.text("Service Name:").ask() + "Flask"

        if new and service:
            services_dir = os.path.join(services_dir, service)
            os.mkdir(services_dir)
            new = True

        service_files_dir = os.path.join(services_dir, service)
        if new:
            click.echo("Creating new Cron service...")
            cron_quickstart(service, services_dir)

    cron_tasks = [
        "(run) - Run a cron service",
        "(test) - Tests the cron service",
        "(build) - Builds the cron service",
        "(test-create) - Create any missing tests for service",
    ]

    task = None
    if not test and not type:
        task = questionary.select(
            "What action would you like to take?", choices=cron_tasks
        ).ask()
        task = task.split(" ")[0].replace("(", "").replace(")", "")
    elif type:
        task = type

    if not service.endswith("Cron"):
        click.echo("💔 You can't use the flask command to run non flask services!")
        exit(1)

    elif task == "test-create":
        test_builder(type_="service", path=service)
    elif task == "build":
        container_builder(service=service, all=False)
    elif task == "run":
        cron_runner(service)
    elif task == "test" or test:
        test_runner(service, all=all, test_path=test)


@builder.command()
def format():
    """Formats every single line of code, ensuring that each and every language we use is up to standard!"""
    import subprocess

    ignore_patterns = [
        ".git/",
        ".svn/",
        ".hg/",
        "node_modules/.*",
        "venv/.*",
        "__pycache__/.*",
        ".mypy_cache/.*",
        "templates/.*",
    ]

    # Construct the exclude pattern for black
    black_exclude_pattern = "|".join([f"{pattern}" for pattern in ignore_patterns])

    # Define the formatter commands
    formatter_commands = [
        f"black . --exclude '{black_exclude_pattern}'",
        "npx prettier '**/*.{js,ts,mjs,cjs,json}' --write",
        "swiftformat .",
    ]

    for command in formatter_commands:
        subprocess.run(command, shell=True, check=True)


@builder.command()
@click.option(
    "--service",
    "-s",
    help="The service to deploy.",
    required=False,
    type=str,
)
def deploy(service):
    """Deploys & Rotates the versionId of the service (If the `prod` and `dev` aren't in sync)"""
    services_dir = get_service_dir()
    service_path = os.path.join(services_dir, service)

    dockerfile_path = os.path.join(service_path, "Dockerfile")
    if os.path.exists(dockerfile_path):
        build_container(service.lower(), dockerfile_path, should_stream_output=True)

        push_image(service.lower())

    deploy_image(service.lower(), service_path)


@builder.command()
def bootstrap():
    bootstrap_command()


if __name__ == "__main__":
    builder()
