import ast
import importlib
import json
import os
import sys
import unittest

import click
import questionary

from bunker_src.utils import config_path
from bunker_src.ui.choose_or_make_dir import choose_or_make_dir


def get_top_level_function_names(file_path: str):
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)

    top_level_function_names = [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.col_offset < 1
    ]

    return top_level_function_names


def get_top_level_class_methods(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)

    class_methods: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            for body_item in node.body:
                if isinstance(body_item, ast.FunctionDef):
                    method_name = body_item.name
                    class_methods.append(f"CLASS/{class_name}/{method_name}")

    return class_methods


def test_builder(type_, path, dir_path="", tests_path=""):
    if tests_path:
        click.echo(f"ℹ Generating Tests for {tests_path}")

    if not dir_path:
        config = json.load(open(config_path))
        services_dir = config.get("create", {}).get("service_dir", {})

        if not services_dir:
            services_dir = choose_or_make_dir("services", ".", False)

        match type_:
            case "service":
                dir_path = os.path.join(services_dir, path)
                tests_path = os.path.join(dir_path, "BunkerTests")
            case "src":
                dir_path = path
                tests_path = os.path.join(path, "BunkerTests")

        if not os.path.exists(tests_path):
            os.mkdir(tests_path)

    excluded = ["venv", "__pycache__", "__init__.py"]

    # List the root dir
    content = os.listdir(dir_path)

    for item in content:
        if item in excluded:
            continue

        item_path = os.path.join(dir_path, item)
        item_type = "file" if os.path.isfile(item_path) else "dir"
        test_dir = os.path.join(tests_path, item).replace(".py", "")

        # Ensure the filename doesn't have BunkerTest inside of it (Directories included)
        if "BunkerTest" in item_path:
            continue

        if item_type == "dir":
            if not os.path.exists(test_dir):
                os.mkdir(test_dir)

            test_builder(
                type_=type_, path=path, dir_path=item_path, tests_path=test_dir
            )

        if item_type == "file" and item_path.split(".")[-1] == "py":
            if not os.path.exists(test_dir):
                os.mkdir(test_dir)

            # Get all the functions
            functions = get_top_level_function_names(item_path)
            class_methods = get_top_level_class_methods(item_path)
            functions += class_methods

            # Create a new file for each function
            for function in functions:
                if function.startswith("CLASS"):
                    segments = function.split("/")

                    if "/CLASS" in test_dir:
                        test_dir = "/".join(test_dir.split("/")[:-1])

                    if not test_dir.endswith("".join(segments[:2])):
                        class_path = os.path.join(
                            test_dir, "".join(segments[:2])
                        )
                        if not os.path.exists(class_path):
                            os.mkdir(class_path)
                        test_dir = class_path

                    function = segments[-1].replace("__", "").capitalize()
                    if function == "init":
                        function = function.upper()

                function_path = os.path.join(test_dir, f"{function}.py")

                if os.path.exists(function_path):
                    continue

                with open(function_path, "w") as f:
                    file_base_content = open(
                        "templates/UnitTestTemplate.py", "r"
                    ).read()
                    test_name_ = item_path.replace(".py", "").split("/")
                    test_name_ += [function]
                    test_name = "".join(
                        [
                            i.replace("(", "").replace(")", "").capitalize()
                            for i in test_name_
                        ]
                    )
                    file_base_content = file_base_content.replace(
                        "<<test_name>>", test_name
                    )
                    f.write(file_base_content)


def test_runner(service: str, test_path="", all=False):
    config = json.load(open(config_path))
    services_dir = config.get("create", {}).get("service_dir", {})

    if not services_dir:
        services_dir = choose_or_make_dir("service", ".")

    if not service and not test_path:
        services_dir = os.path.join(services_dir)
        service = questionary.select(
            f"Which test do you want to run?", choices=os.listdir(services_dir)
        ).ask()

    if service and test_path:
        service_tests_path = os.path.join(services_dir, service, "BunkerTests")
        test_path = os.path.join(service_tests_path, test_path)

    if not test_path:
        service_tests_path = os.path.join(services_dir, service, "BunkerTests")

        if not os.path.exists(service_tests_path):
            click.echo(f"😥 There are no tests for service {service}")
            return

        path_ = service_tests_path
        while True:
            if all:
                test_path = os.path.join(path_)
                break

            files_in_dir = os.listdir(path_) + [
                "Run All Tests in This Directory"
            ]

            choice = questionary.select(
                "Choose Tests to Run: ", choices=files_in_dir
            ).ask()

            if choice == "Run All Tests in This Directory":
                test_path = os.path.join(path_)
                break

            if choice.endswith(".py"):
                test_path = os.path.join(path_, choice)
                break

            path_ = os.path.join(path_, choice)
        click.echo(
            f"ℹ If you want to run this same test again, Use this command \n python bunker.py test --test {test_path}"
        )

    def run_tests(file_path):
        tests_passed = False
        if file_path.endswith(".py"):
            module_name = os.path.splitext(file_path.split("/")[-1])[0]

            # Run the tests in the specific file
            try:
                spec = importlib.util.spec_from_file_location(
                    module_name, file_path
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for name in dir(module):
                    obj = getattr(module, name)
                    if isinstance(obj, type) and issubclass(
                        obj, unittest.TestCase
                    ):
                        # Load tests from the TestCase class
                        loader = unittest.TestLoader()
                        suite = loader.loadTestsFromTestCase(obj)

                        runner = unittest.TextTestRunner()
                        result = runner.run(suite)

                        if not result.wasSuccessful():
                            tests_passed = False
                        else:
                            tests_passed = True

            except Exception as e:
                click.echo(f"Error loading tests from {file_path}: {e}")
                tests_passed = False

            return tests_passed

    all_tests_passed = True
    if test_path.endswith(".py") and "BunkerTests" in test_path:
        all_tests_passed = run_tests(test_path)

    for root, _, files in os.walk(test_path):
        for file in files:
            file_path = os.path.join(root, file)
            if "BunkerTests" in file_path:
                all_tests_passed = run_tests(file_path)

    if not all_tests_passed:
        click.echo("🥲 Some of your tests failed! Write better code!")
        sys.exit(1)
