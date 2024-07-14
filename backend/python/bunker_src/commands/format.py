import subprocess


def main():

    ignore_patterns = [
        ".git/",
        ".svn/",
        ".hg/",
        "node_modules/.*",
        "venv/.*",
        "__pycache__/.*",
        ".mypy_cache/.*",
        "templates/.*",
    ]

    # Construct the exclude pattern for black
    black_exclude_pattern = "|".join([f"{pattern}" for pattern in ignore_patterns])

    # Define the formatter commands
    formatter_commands = [
        f"black . --exclude '{black_exclude_pattern}'",
        "npx prettier '**/*.{js,ts,mjs,cjs,json}' --write",
        "swiftformat .",
    ]

    for command in formatter_commands:
        subprocess.run(command, shell=True, check=True)
