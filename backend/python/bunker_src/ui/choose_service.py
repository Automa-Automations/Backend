import json
import os

import questionary
from bunker_src.utils import get_service_dir


def choose_service():
    service_dir = get_service_dir()

    services = os.listdir(service_dir)
    service = questionary.select("Select a service: ", choices=services).ask()

    return service