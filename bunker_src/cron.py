import datetime
import json
import os
import uuid

import click
from bunker_src.docker import container_builder, container_runner
from bunker_src.utils import config_path
from croniter import croniter


def cron_quickstart(name: str, service_path: str):
    os.system(f"cp -r templates/Cron/* {service_path}")
    config = json.load(open(os.path.join(service_path, "config.json")))
    config["name"] = f"{name}-{uuid.uuid4().hex}".lower()

    dockerfile_path = os.path.join(service_path, "Dockerfile")
    if not os.path.exists(dockerfile_path):
        click.echo("Dockerfile not found. Using default Dockerfile.")
        os.system(f"cp templates/Flask/Dockerfile {dockerfile_path}")

    click.echo("📝 Modifying Dockerfile...")
    dockerfile = open(dockerfile_path).read()
    dockerfile = dockerfile.replace("<<app_run>>", "cd " + service_path + "; ")
    open(dockerfile_path, "w").write(dockerfile)

    click.echo("📝 Modifying main.py...")
    main_path = os.path.join(service_path, "main.py")
    main = open(main_path).read()
    open(main_path, "w").write(main)

    click.echo("🚀 Cron service created.")


def cron_runner(service):

    config = json.load(open(config_path))
    services_dir = config.get("create", {}).get("service_dir", {})
    service_path = os.path.join(services_dir, service)
    service_config_path = os.path.join(service_path, "config.json")
    service_config = json.load(open(service_config_path))

    container_builder(service, all=False)

    schedule = service_config["schedule"]

    schedule = "0 * * * *" if schedule == "hourly" else schedule
    schedule = "0 0 * * *" if schedule == "daily" else schedule
    schedule = "0 0 1 * *" if schedule == "monthly" else schedule
    schedule = "0 0 * * 1" if schedule == "weekly" else schedule

    iter = croniter(schedule)
    next = iter.get_next()

    while True:
        current_time = datetime.datetime.now().timestamp()

        if current_time >= next and current_time - next < 5:
            click.echo(f"🏃‍Running Cron Service at {current_time}")
            next = iter.get_next()
            container_runner(service)
