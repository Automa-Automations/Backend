# Bunker is a build, template, configuration and auto testing for unit tests, integration tests & production tests.
# Bunker will allow you to generate templates for projects, allowing you to effectively test every single method of a class, every single module & every single package that you are developoing. bunker will also create a generic template for each service, and also create templates for any service your service depends on, in order to test them with each other "integration tests". bunker will also create a template for the production environment, and will allow you to test your service with the production environment, to ensure that your service is working as expected. bunker will also create a template for the production environment, and will allow you to test your service with the production environment, to ensure that your service is working as expected. bunker will also create a template for the production environment, and will allow you to test your service with the production environment, to ensure that your service is working as expected. bunker also effectively injects code into your project to do monitoring, bunker captures all logs into a single generic database, and also captures errors, uptime, usage & more.
import click
from bunker_src.commands.create_command import main as create_command
from bunker_src.commands.cron_builder import main as cron_builder
from bunker_src.commands.deploy_command import main as deploy_command
from bunker_src.commands.flask_command import main as flask_command
from bunker_src.commands.format import main as format_command
from bunker_src.initialization import main as initialization

initialization()

import os

from bunker_src.commands.bootstrap import command as bootstrap_command
from bunker_src.docker import container_builder, container_runner
from bunker_src.testing import test_builder, test_runner
from bunker_src.ui.choose_service import choose_service
from bunker_src.utils import global_options
from colorama import init

os.environ["DOCKER_BUILDKIT"] = "1"

init(autoreset=True)


@click.group()
@global_options
def builder():
    """Bunker's code building CLI."""
    pass


@builder.command()
def create():
    """Create a new service from template. Or from scratch."""
    create_command()


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
@click.option("--service", "-s", help="The service to run.", required=False, type=str)
@click.option(
    "--rebuild",
    "-r",
    help="Rebuilds the service before running",
    required=False,
    is_flag=True,
)
def run(service, rebuild):
    """Allows you to run a service if it exists,"""
    if not service:
        service = choose_service()

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
def flask(service, new, test, route):
    """Utility to generate flask templates, routes, files & tests"""
    flask_command(service, test, new, route)


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
def cron(service, test, new, all):
    """
    Allows you to generate cron services, run them, test them and build them.
    """
    cron_builder(service, test, new, all)


@builder.command()
def format():
    """Formats every single line of code, ensuring that each and every language we use is up to standard!"""
    format_command()


@builder.command()
@click.option(
    "--service",
    "-s",
    help="The service to deploy.",
    required=False,
    type=str,
)
@click.option(
    "--build",
    "-b",
    help="If we should directly build the container, or use a cached version",
    required=False,
    type=bool,
)
def deploy(service, build=True):
    """Deploys & Rotates the versionId of the service (If the `prod` and `dev` aren't in sync)"""
    deploy_command(service, build)


@builder.command()
def bootstrap():
    """Bootstraps the project + structure to ensure no akward behaviour occurs!"""
    bootstrap_command()


if __name__ == "__main__":
    builder()
