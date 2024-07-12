import json
import os
import uuid
from typing import Any

import click
import docker
import questionary
from bunker_src.ui.ask_config import ask_config_json_questions
from bunker_src.ui.choose_or_make_dir import choose_or_make_dir
from bunker_src.utils import config_path, get_exposed_ports, get_service_dir
from colorama import Fore
from yaspin import yaspin


def dockerhub_quickstart(name: str, root_dir: str):
    client = docker.from_env()
    image = questionary.text("Docker Image:").ask()

    if not image:
        click.echo("Docker image cannot be empty.")
        return

    with yaspin(text=f"🔍 Searching for {image}") as sp:
        response: Any = client.images.search(image)
        if not response:
            sp.fail("No image found.")
            return
        else:
            sp.text = f"✅ Found {len(response)} images for {image}"
            sp.start()

        image_to_use = questionary.select(
            "Select an image:", choices=[f'{x["name"]}' for x in response]
        ).ask()
        if not image_to_use:
            click.echo("No image selected.")
            return

    click.echo(f"🚀 Creating {name} service from {image_to_use}")

    # Create the service
    config: dict[str, Any] = {
        "base_image": image_to_use,
        "name": f"{name.lower()}-{uuid.uuid4().hex}".lower(),
        "cpu": 0,
        "memory": 0,
        "gpu": "",
        "ports": {},
        "mounts": {},
        "env": {},
    }
    # Save the config
    click.echo("📝 Saving configuration...")

    # PORTS (Auto Detectable)
    click.echo("🔍 Detecting ports...")
    ports_ = get_exposed_ports(image_to_use)
    ports = {str(port.split("/")[0]): str(port.split("/")[0]) for port in ports_}

    for port in ports_:
        click.echo(f"   🛶 {Fore.YELLOW} Detected port {port}")

    config["ports"] = ports

    config = ask_config_json_questions(config)

    click.echo("📝 Saving configuration...")
    json.dump(config, open(os.path.join(root_dir, "config.json"), "w"), indent=4)


def build_container(
    service: str, dockerfile_path: str, should_stream_output: bool = False
) -> str:
    client = docker.APIClient()
    try:
        stream = client.build(
            path=os.path.abspath("."),
            tag=f"{os.environ['DOCKERHUB_USERNAME']}/{service.lower()}",
            dockerfile=dockerfile_path,
            decode=True,
        )

        spinner = None
        for line in stream:
            if line.get("stream"):
                if "stream" not in line.keys():
                    continue

                if "--->" in line["stream"]:
                    continue

                if "Successfully tagged" in line["stream"]:
                    if spinner:
                        spinner.stop()
                        spinner.ok("✅")
                    return line["stream"].split(" ")[-1].strip().replace("\n", "")

                if not should_stream_output:
                    continue

                if line["stream"].strip() == "":
                    continue

                pretty_output = (
                    line["stream"].encode("utf-8").decode("unicode-escape").strip()
                )
                pretty_output = pretty_output.replace("â", "").replace(
                    "WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv",
                    "",
                )

                if "[notice] A new release of pip" in pretty_output:
                    continue

                # Remove anything that is not ASCII
                pretty_output = "".join(
                    [i if ord(i) < 128 else " " for i in pretty_output]
                )

                if len(":".join(pretty_output.split(":")[1:]).strip()) == 0:
                    continue

                if not spinner:
                    spinner = yaspin(text=f"{pretty_output}")
                    spinner.start()

                if "Step" in pretty_output:
                    spinner.stop()
                    spinner.ok("✅")
                    spinner = yaspin(text=f"{pretty_output}")
                    spinner.start()
                else:
                    spinner.text = (
                        f"{spinner.text.split(':')[0]}: {pretty_output[:50]}..."
                    )

            if "error" in line:
                click.echo(f"{Fore.RED}Error: {line['error']}", err=True)
                break
    # Ignore mypy error
    # mypy: ignore
    except docker.errors.BuildError as e:
        click.echo(f"{Fore.RED}BuildError: {e}", err=True)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)

    return ""


def container_builder(service: str, all: bool):
    global config_path
    services = []
    # Get the services directory
    services_dir = get_service_dir()
    services_in_service_dir = os.listdir(services_dir)

    if all:
        services = os.listdir(services_dir)

    if not service and not all:
        service = questionary.select(
            "Select a service to build:", choices=services_in_service_dir
        ).ask()
        services = [service]
    elif service:
        services = [service]

    for service in services:
        service_path = os.path.join(services_dir, service)

        if not os.path.isdir(service_path):
            continue

        click.echo(f"{Fore.GREEN}Building Docker image for service: {service}")
        dockerfile_path = os.path.join(service_path, "Dockerfile")
        config_path_ = os.path.join(service_path, "config.json")
        service_name = json.load(open(config_path_)).get("name", uuid.uuid4().hex)

        df_exists = os.path.exists(dockerfile_path)
        cf_exists = os.path.exists(config_path_)

        if not df_exists and not cf_exists:
            click.echo(
                f"❌{Fore.RED}Error: Dockerfile and Config does not exist at path {service_path}"
            )
            return

        if df_exists and not cf_exists:
            click.echo(
                f"❌{Fore.RED}Error: Dockerfile but Config file doesn't exist. Deployment isn't possible!"
            )
            return

        if not df_exists and cf_exists:
            click.echo(f'🎉 {service} is a "Deploy Only" container!')
            continue

        click.echo(
            f"{Fore.GREEN}🎉 Built Image: {build_container(service_name, dockerfile_path)}"
        )


def container_runner(service: str, rebuild=False):
    if not service:
        click.echo(
            "😥 Sorry, But it doesn't seem that you provided a valid service name!"
        )
        exit(1)

    services_dir = get_service_dir()

    client = docker.from_env()

    image = [
        i
        for i in client.images.list()
        if i.attrs["RepoTags"] and i.attrs["RepoTags"][0] == f"{service.lower()}:latest"
    ]

    if not image or rebuild:
        container_builder(service=service, all=False)

    with yaspin(text=f"⤵️ Starting the Container running Process...") as sp:
        if not services_dir:
            services_dir = choose_or_make_dir("services", ".", False)

        if not service:
            service = questionary.select(
                "Select a service to run:", choices=os.listdir(services_dir)
            ).ask()

        service_path = os.path.join(services_dir, service)
        service_config_path = os.path.join(service_path, "config.json")

        if not os.path.exists(service_path):
            sp.fail("😥 Please run a valid service!")
            exit(1)

        service_config = json.load(open(service_config_path))

        ports = service_config.get("ports", {})
        mounts = service_config.get("mounts", {})
        env = service_config.get("env", {})
        base_image = service_config.get("base_image")

        image = service_config.get("name").lower() if not base_image else base_image

        ports_transformed = {
            str(internal) + "/tcp": str(external)
            for internal, external in ports.items()
        }

        mounts_transformed = []
        for mount_name, mount_location in mounts.items():
            mounts_transformed.append(
                docker.types.Mount(
                    target=mount_location.split(":", 0),
                    source=mount_name,
                    type="volume",
                    size=mount_location.split(":")[1],
                )
            )

        containers = client.containers.list(all=True)
        for container in containers:
            if container.name == service:
                sp.text = "🐳 Container already existed. Killing Previous Instance"
                container.stop()
                container.remove()
                break

        sp.text = f"🐳 Starting {service}..."
        container = client.containers.run(
            image=f"{os.environ['DOCKERHUB_USERNAME']}/{image}",
            name=service,
            ports=ports_transformed,
            mounts=mounts_transformed,
            environment=env,
            detach=True,
        )

        sp.text = "Container successfully started running!"
        sp.ok("🎉")

        for message in container.logs(stream=True):
            formatted_message = (
                f"    {Fore.LIGHTBLACK_EX}{message.decode('utf-8').strip()}"
            )
            print(formatted_message)

        click.echo("🎉 Container Job successfully Finished!")

    return container


def is_service_running(service) -> bool:
    client = docker.from_env()
    try:
        container = client.containers.get(service)
        if not container:
            return False

        container_state = container.attrs["State"]
        return container_state["Status"] == "running"
    except docker.errors.NotFound:
        return False


def push_image(image_name):
    client = docker.from_env()
    if "/" not in image_name:
        repository = f"{os.environ['DOCKERHUB_USERNAME']}/{image_name}"
    else:
        repository = image_name

    click.echo(f"Starting to push the image {repository}...")

    try:
        with yaspin(text="Pushing image", color="cyan") as spinner:
            push_output = client.images.push(repository, stream=True, decode=True)
            for line in push_output:
                status_message = "Pushing image"
                if "status" in line:
                    status_message = line["status"]
                    if "id" in line:
                        status_message = (
                            f"Layer ID: {line['id']}, Status: {line['status']}"
                        )
                    spinner.text = status_message

                if "progress" in line:
                    spinner.text = f"{status_message} - Progress: {line['progress']}"

                if "error" in line:
                    spinner.fail("❌")
                    click.echo(f"Error: {line['error']}", err=True)
                    return

            spinner.ok("✅")
            click.echo(f"🎉 Finished pushing the image {Fore.GREEN}{repository}.")

    except docker.errors.APIError as e:
        click.echo(f"APIError: {e}", err=True)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
