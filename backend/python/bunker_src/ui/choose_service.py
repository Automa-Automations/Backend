import os

import click
import questionary
from bunker_src.utils import get_service_dir


def choose_service():
    service_dir = get_service_dir()

    services = os.listdir(service_dir)
    if not services:
        click.echo(
            "😥 There aren't any services to run! Create one using the 'create' command!"
        )
        exit(1)

    service = questionary.select("Select a service: ", choices=services).ask()

    return service
