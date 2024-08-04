import json
import os
import uuid

import click
import questionary
from bunker_src.utils import get_service_dir
from yaspin import yaspin


def flask_quickstart(name: str, root_dir: str):
    os.system(f"cp -r templates/Flask/* {root_dir}")
    config = json.load(open(os.path.join(root_dir, "config.json")))
    config["name"] = f"{name}-{uuid.uuid4().hex}".lower()

    dockerfile_path = os.path.join(root_dir, "Dockerfile")
    if not os.path.exists(dockerfile_path):
        click.echo("Dockerfile not found. Using default Dockerfile.")
        os.system(f"cp templates/Flask/Dockerfile {dockerfile_path}")

    click.echo("📝 Modifying Dockerfile...")
    dockerfile = open(dockerfile_path).read()
    dockerfile = dockerfile.replace("<<port>>", list(config["ports"].keys())[0])
    dockerfile = dockerfile.replace(
        "<<app_run>>", "cd " + os.path.join(root_dir) + "; "
    )
    open(dockerfile_path, "w").write(dockerfile)

    click.echo("📝 Modifying main.py...")
    main_path = os.path.join(root_dir, "main.py")
    main = open(main_path).read()
    main = main.replace("<<port>>", list(config["ports"].keys())[0])
    open(main_path, "w").write(main)

    click.echo("🚀 Flask service created.")


def ask_flask_route_config():
    config = {"route": questionary.text("What route would you like to create?").ask()}

    return config


def flask_route_builder(service, all, route=""):
    if not route:
        route = ask_flask_route_config()["route"]

    routes = route.split("/")

    if routes[0] != "":
        routes = [""] + routes

    services_dir = get_service_dir()
    service_path = os.path.join(services_dir, service)

    routes_path = os.path.join(service_path, "pages")
    types_of_routes = ["post", "put", "get", "delete"]

    with yaspin(text=f"⤵️ Building Routes...") as sp:
        for route in routes:
            routes_path = os.path.join(routes_path, route)
            sp.text = f"Building Route {routes_path}"

            if not os.path.exists(routes_path):
                os.mkdir(routes_path)

            if not os.listdir(routes_path):
                files_to_create = [
                    os.path.join(routes_path, f"index({rt}).py")
                    for rt in types_of_routes
                ]

                for file in files_to_create:
                    file_ = open(file, "w")
                    file_.write(f'def default(): return "Hello, {file}"')
