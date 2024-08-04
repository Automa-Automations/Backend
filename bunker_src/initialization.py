import os

import click
import dotenv
import questionary


def main():
    if not os.path.exists(".bunker.env"):
        click.echo(
            "Sorry, But it doesn't seem that you have your environment variables configured!"
        )
        with open(".bunker.env", "w") as f:
            f.write(
                f"""
    DOCKERHUB_USERNAME="{questionary.text('What is your DockerHub username?').ask()}"
    DOCKERHUB_PASSWORD="{questionary.text('What is your DockerHub password?').ask()}"
    FLY_IO_API_KEY="{questionary.text('What is your fly.io API key?').ask()}"
            """
            )

    dotenv.load_dotenv(".bunker.env")
