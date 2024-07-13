import os

from bunker_src.docker import build_container, push_image
from bunker_src.fly_io import deploy_image
from bunker_src.utils import get_service_dir


def main(service: str):
    services_dir = get_service_dir()
    service_path = os.path.join(services_dir, service)

    dockerfile_path = os.path.join(service_path, "Dockerfile")
    if os.path.exists(dockerfile_path):
        build_container(service.lower(), dockerfile_path, should_stream_output=True)

        push_image(service.lower())

    deploy_image(service.lower(), service_path)
