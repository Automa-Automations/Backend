import json
import os

import click
import questionary
from bunker_src.commands.sqs_quickstart import main as sqs_quickstart
from bunker_src.cron import cron_quickstart
from bunker_src.docker import dockerhub_quickstart
from bunker_src.flask import flask_quickstart
from bunker_src.utils import get_service_dir


def main():
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
                "SQS - A simple SQS Template that is very extendible + functional",
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
        if (
            template
            == "SQS - A simple SQS Template that is very extendible + functional"
        ):
            os.mkdir(service_path + "SQS")
            sqs_quickstart(name, service_path + "SQS")
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

    click.echo(
        "✅ Please check out the fly.toml file that was created. You can leverage that to modify the service! If none was created, take a look at the template fly.toml file, or directly run 'fly launch' command in terminal to get started!"
    )
