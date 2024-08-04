import os

import click
from bunker_src.docker import build_container, push_image
from bunker_src.fly_io import deploy_image
from bunker_src.utils import get_service_dir


def main(service: str, build: bool):
    services_dir = get_service_dir()
    service_path = os.path.join(services_dir, service)

    dockerfile_path = os.path.join(service_path, "Dockerfile")
    if os.path.exists(dockerfile_path) and build:
        click.echo("🌍 Building Container...")
        build_container(service.lower(), dockerfile_path, should_stream_output=True)

    click.echo("🌍 Pushing to DockerHUB")
    push_image(service.lower())

    click.echo("🌍 Deploying...")
    deploy_image(service.lower(), service_path)
