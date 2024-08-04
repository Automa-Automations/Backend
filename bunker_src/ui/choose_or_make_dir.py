import os

import questionary


def choose_or_make_dir(type: str, root_dir: str, make_new: bool = True):
    root_dir_files = os.listdir(root_dir)
    if make_new:
        create_or_choose = questionary.select(
            f"Would you like to create a new {type} directory or choose an existing one?",
            choices=["Create", "Choose"],
        ).ask()
    else:
        create_or_choose = "Choose"

    if create_or_choose == "Choose":
        root_dir = questionary.select(
            "Select a root directory:", choices=root_dir_files
        ).ask()
    else:
        root_dir = questionary.text(
            f"{type.capitalize()} Directory Name:"
        ).ask()
        os.mkdir(root_dir)

    return root_dir
