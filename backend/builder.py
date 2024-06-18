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
 
def docker_command_builder(container_name: str, config_path: str):
    config = json.load(open(config_path))

    if not container_name:
        container_name = config['base_image']

    run_command = "docker run -d "
    if "mounts" in config:
        for (mount_name, mount_path) in config['mounts'].items():
            run_command += f"-v {mount_name}:{mount_path} "

    if "networking" in config:
        if "http" in config["networking"]:
            ports = config['networking']['http'].items()
            for (internal, external) in ports:
                run_command += f"-p {external}:{internal} "
                
    if "specs" in config:
        specs = config['specs']
        if "cpu" in specs:
            run_command += f"--cpus {specs['cpu']} "
            
        if "memory" in specs:
            run_command += f"--memory {specs['memory']}MB "

        if "gpu" in specs:
            if "auto" in specs["gpu"]:
                run_command += "--gpus auto "

    run_command += container_name

    return run_command


if __name__ == "__main__":
    services_path = 'services'
    services = list_services(services_path)
    for service in services:
        service_dir_path = os.path.join(services_path, service)
        ctype = container_type(services_path, service)
        container_name = ''
        if ctype == ContainerType.DOCKER:
            container_name = build_docker(service_dir_path, service)
        elif ctype == ContainerType.CONFIG:
            # We need to use the config.json to ensure everything works (AKA, we use config.json to directly run a container instead of needing to build, but in the future we will make it have fly.io deploy options etc... )
            print('Config file found, not building anything')
            
        config_path = os.path.join(service_dir_path, 'config.json')
        if not os.path.exists(config_path):
            print("No config file found, skipping")
            continue

        os.system(docker_command_builder(container_name, config_path))
