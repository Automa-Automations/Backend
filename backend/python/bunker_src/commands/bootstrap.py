# The bootstrap command will quickly build out a config file for the project

import json
import os

import click
import questionary


def command():
    if not os.path.exists("services"):
        os.mkdir("services")

    if not os.path.exists("config.json"):
        with open("config.json", "w") as f:
            base_config = {
                "create": {"service_dir": "services"},
            }

            f.write(json.dumps(base_config))

        click.echo(
            "Please be reminded to fill in all the requirements in the .bunker.env file!"
        )
