from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda_python_alpha as python,
    aws_lambda,
    # aws_sqs as sqs,
)
from aws_cdk import aws_apigateway
from constructs import Construct
from dotenv import dotenv_values
import subprocess
import os

environment_variables = dict(dotenv_values(".env"))

class BackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Execute the script to install dependencies
        subprocess.run(["./install_packages.sh"], check=True)

        stripe_payment_sheet = python.PythonFunction(
           self,
            "stripe-payment-sheet",
            entry="./backend/python",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="handler",
            index="lambdas/stripe/payment_sheet.py",
            bundling=python.BundlingOptions(
                asset_excludes=["venv"],
            ),
            environment=environment_variables,
        )

        stripe_event_webhook = python.PythonFunction(
            self,
            "stripe-event-webhook",
            entry="./backend/python",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="handler",
            index="lambdas/stripe/webhook.py",
            bundling=python.BundlingOptions(asset_excludes=["venv"]),
            environment=environment_variables,
        )

        auto_configure_app = python.PythonFunction(
            self,
            "auto-configure-app",
            entry="./backend/python",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="handler",
            index="lambdas/config/auto_config_mobile_app.py",
            bundling=python.BundlingOptions(asset_excludes=["venv"]),
            environment=environment_variables,
        )

        podcast_to_shorts_lambda = python.PythonFunction(
            self,
            "podcast_to_shorts_lambda",
            entry="./backend/python",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="handler",
            index="lambdas/bots/podcast_to_shorts.py",
            bundling=python.BundlingOptions(asset_excludes=["venv"]),
            environment=environment_variables,
        )


        # add new python environment
        stripe_payment_sheet.add_environment("PYTHONPATH", "/var/task/lambdas/packages:" + os.environ.get("PYTHONPATH", ""))
        stripe_event_webhook.add_environment("PYTHONPATH", "/var/task/lambdas/packages:" + os.environ.get("PYTHONPATH", ""))
        auto_configure_app.add_environment("PYTHONPATH", "/var/task/lambdas/packages:" + os.environ.get("PYTHONPATH", ""))
        podcast_to_shorts_lambda.add_environment("PYTHONPATH", "/var/task/lambdas/packages:" + os.environ.get("PYTHONPATH", ""))

        # In our requests we will add this to the headers
        api = aws_apigateway.RestApi(
            self,
            "backend-generic-api",
            rest_api_name="backend-generic-api",
            default_cors_preflight_options={
                "allow_origins": aws_apigateway.Cors.ALL_ORIGINS
            },
        )

        # Payment Sheet Endpoint
        stripe_endpoint = api.root.add_resource("stripe")
        payment_sheet = stripe_endpoint.add_resource("payment-sheet")
        payment_sheet_integration = aws_apigateway.LambdaIntegration(
            stripe_payment_sheet
        )
        payment_sheet.add_method("POST", payment_sheet_integration)

        # Success webhook endpoint
        stripe_event_webhook_integration = aws_apigateway.LambdaIntegration(
            stripe_event_webhook
        )
        webhook = stripe_endpoint.add_resource("webhook")
        webhook.add_method("POST", stripe_event_webhook_integration)

        # Auto configure app endpoint
        config_endpoint = api.root.add_resource("config")
        auto_configure_app_integration = aws_apigateway.LambdaIntegration(
            auto_configure_app
        )
        auto_configure_app_resource = config_endpoint.add_resource("config_mobile_app")
        auto_configure_app_resource.add_method("GET", auto_configure_app_integration)

        # --- BOTS ---

        bots_endpoint = api.root.add_resource("bots")
        podcast_to_shorts = bots_endpoint.add_resource("podcast_to_shorts")
        podcast_to_shorts_integration = aws_apigateway.LambdaIntegration(
            podcast_to_shorts_lambda
        )
        podcast_to_shorts.add_method("POST", podcast_to_shorts_integration)
