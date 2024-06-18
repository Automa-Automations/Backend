import json
import docker
import os
from enum import Enum

class ContainerType(Enum):
    DOCKER = 'docker'
    CONFIG = 'config'
    INVALID = 'invalid'

def list_services(path: str) -> list:
    return os.listdir(path)


def check_deploy_type(docker_file, config_file):
    if os.path.exists(docker_file):
        return ContainerType.DOCKER
    elif os.path.exists(config_file):
        return ContainerType.CONFIG
    else:
        return ContainerType.INVALID

def container_type(services_path, service: str) -> ContainerType:
    docker_file = os.path.join(services_path, service, 'Dockerfile')
    config_file = os.path.join(services_path, service, 'config.json')
    return check_deploy_type(docker_file, config_file)

def build_docker(service_dir_path: str, service: str):
    print(f'Building docker container for {service}')
    client = docker.from_env()
    client.images.build(path=service_dir_path, tag=service.lower())
    return service.lower()
 
if __name__ == "__main__":
    services_path = 'services'
    services = list_services(services_path)
    for service in services:
        service_dir_path = os.path.join(services_path, service)
        if container_type(services_path, service) == ContainerType.DOCKER:
            build_docker(service_dir_path, service)
        else:
            print(f'Invalid container type for {service}')
