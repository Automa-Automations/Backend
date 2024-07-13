import os

import click
import questionary
from bunker_src.cron import cron_quickstart, cron_runner
from bunker_src.docker import container_builder
from bunker_src.testing import test_builder, test_runner
from bunker_src.utils import get_service_dir


def main(service, test, new, all):
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
                choices=[i for i in os.listdir(services_dir) if i.endswith("Flask")],
            ).ask()
        elif new and not service:
            service = questionary.text("Service Name:").ask() + "Flask"

        if new and service:
            services_dir = os.path.join(services_dir, service)
            os.mkdir(services_dir)
            new = True

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
