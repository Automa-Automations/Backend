import json
import os

import questionary

from bunker_src.utils import config_path
from bunker_src.ui.choose_or_make_dir import choose_or_make_dir


def choose_service():
    config = json.load(open(config_path))

    service_dir = config.get("create", {}).get("service_dir", {})

    if not service_dir:
        service_dir = choose_or_make_dir("services", ".")

        save_default = questionary.confirm(
            "Would you like to save this as the default service directory?"
        ).ask()

        if save_default:
            config["create"]["service_dir"] = service_dir
            json.dump(config, open(config_path, "w"), indent=4)

    services = os.listdir(service_dir)
    service = questionary.select("Select a service: ", choices=services).ask()

    return service
