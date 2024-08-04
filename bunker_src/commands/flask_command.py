import os

import click
import questionary
from bunker_src.docker import container_builder, container_runner
from bunker_src.flask import flask_quickstart, flask_route_builder
from bunker_src.ngrok import ngrok_container
from bunker_src.testing import test_builder, test_runner
from bunker_src.ui.choose_service import choose_service
from bunker_src.utils import get_service_dir


def main(service, test, new, route):
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
            service = choose_service()
        elif new and not service:
            service = questionary.text("Service Name:").ask() + "Flask"

        if new and service:
            services_dir = os.path.join(services_dir, service)
            os.mkdir(services_dir)
            new = True

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
