from typing import Any

import click
import questionary


def ask_config_json_questions(config: dict[str, Any]):
    config = config.copy()

    # CPU
    should_ask_cpu = True
    if (
        config["cpu"]
        and not questionary.confirm(
            f"Would you like to change the CPU? ({config['cpu']})"
        ).ask()
    ):
        should_ask_cpu = False

    if should_ask_cpu:
        cpu_cores = ["1", "2", "4", "8", "16", "32"]
        cpu = questionary.select("Select CPU Cores:", choices=cpu_cores).ask()
        config["cpu"] = cpu

    # Memory
    # If there is already memory specified in config then ask the user if they want to change it
    should_ask_memory = True
    can_ask_gpu = True
    if (
        config["memory"]
        and not questionary.confirm(
            f"Would you like to change the memory? ({config['memory']})"
        ).ask()
    ):
        should_ask_memory = False

    if should_ask_memory:
        memory_units = ["MB", "GB"]
        memory_unit = questionary.select(
            "Select Memory Unit:", choices=memory_units
        ).ask()

        memory_amounts_mb = [
            "128",
            "256",
            "512",
            "1024",
            "2048",
            "4096",
            "8192",
            "16384",
            "32768",
            "65536",
        ]
        memory_amounts_gb = ["1", "2", "4", "8", "16", "32", "64"]
        if memory_unit == "MB":
            memory = questionary.select(
                "Select Memory Amount (MB):", choices=memory_amounts_mb
            ).ask()
        else:
            memory = questionary.select(
                "Select Memory Amount (GB):", choices=memory_amounts_gb
            ).ask()

        config["memory"] = f"{memory}{memory_unit}"

        memory_amount = memory if memory_unit == "MB" else memory * 1024
        if int(memory_amount) < 2048:
            can_ask_gpu = False
            config["cpu_mode"] = "shared"
            click.echo(
                f"ℹ Memory is less than 2GB. GPU cannot be enabled for this service."
            )
    # GPU

    should_ask_gpu = True
    if can_ask_gpu:
        if (
            config["gpu"]
            and not questionary.confirm(
                f"Would you like to change the GPU? ({config['gpu']})"
            ).ask()
        ):
            should_ask_gpu = False

        if should_ask_gpu:
            gpus = ["none", "a10", "l40s", "a100-40gb", "a100-80gb"]
            gpu = questionary.select("Select GPU:", choices=gpus).ask()
            config["gpu"] = gpu
            config["cpu_mode"] = "performance" if gpu != "none" else "shared"

    mounts = config.get("mounts", {})
    should_ask_mounts = True
    if mounts and not questionary.confirm("Would you like to change the mounts?").ask():
        should_ask_mounts = False

    if should_ask_mounts:
        should_ask_mounts = questionary.confirm("Would you like to add mounts?").ask()

    if should_ask_mounts:
        while True:
            mount_name = questionary.text("Mount Name:").ask()
            mount_path = questionary.text("Mount Path:").ask()
            mount_size = questionary.text("Mount Size (GB):").ask()

            mounts[mount_name] = f"{mount_path}:{mount_size}"
            add_another = questionary.confirm("Add another mount?").ask()
            if not add_another:
                break

    config["mounts"] = mounts

    # Environment Variables
    env_vars = config.get("env", {}).copy()
    should_ask_env_vars = True
    if (
        env_vars
        and not questionary.confirm(
            "Would you like to change the environment variables?"
        ).ask()
    ):
        should_ask_env_vars = False

    if should_ask_env_vars:
        should_ask_env_vars = questionary.confirm(
            "Would you like to add environment variables?"
        ).ask()

    if should_ask_env_vars:
        while True:
            env_var_name = questionary.text("Environment Variable Name:").ask()
            env_var_value = questionary.text("Environment Variable Value:").ask()
            env_vars[env_var_name] = env_var_value
            add_another = questionary.confirm("Add another environment variable?").ask()
            if not add_another:
                break

    config["env"] = env_vars

    if "schedule" in config:
        schedule_types = ["hourly", "daily", "weekly", "monthly"]
        cron = questionary.select(
            "How often should this service run?", choices=schedule_types
        ).ask()

        config["schedule"] = cron

    click.echo(
        """🌍 If you would like to configure regions, take a look at the 'https://fly.io/docs/reference/regions/' page.
As well as configuring regions in the config.json files as type 'dict.key(region as string[])"""
    )

    return config
