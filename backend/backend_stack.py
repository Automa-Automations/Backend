from aws_cdk import (
    Stack,
    aws_lambda_python_alpha as python,
    aws_lambda,
)
from aws_cdk import aws_apigateway
from constructs import Construct
from dotenv import dotenv_values

environment_variables = dict(dotenv_values(".env"))


class BackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        backend_stack_zip = "./backend/layers/backend_layer.zip"

        backend_stack_layer  = aws_lambda.LayerVersion(
            self,
            "BackendStackLayer",
            code=aws_lambda.Code.from_asset(backend_stack_zip),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_11],
            description="Layer with all python packages required for all lambdas to work.",
        )

        bundlingOptions = python.BundlingOptions(
            asset_excludes=["venv", "__pycache__", "test_assets", "tests", "downloads"],
        )

        stripe_payment_sheet = python.PythonFunction(
            self,
            "stripe-payment-sheet",
            entry="./backend/python",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="handler",
            index="lambdas/stripe/payment_sheet.py",
            bundling=bundlingOptions,
            environment=environment_variables,
            layers=[backend_stack_layer],
        )

        stripe_event_webhook = python.PythonFunction(
            self,
            "stripe-event-webhook",
            entry="./backend/python",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="handler",
            index="lambdas/stripe/webhook.py",
            bundling=bundlingOptions,
            environment=environment_variables,
            layers=[backend_stack_layer],
        )

        auto_configure_app = python.PythonFunction(
            self,
            "auto-configure-app",
            entry="./backend/python",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="handler",
            index="lambdas/config/auto_config_mobile_app.py",
            bundling=bundlingOptions,
            environment=environment_variables,
            layers=[backend_stack_layer],
        )

        podcast_to_shorts_lambda = python.PythonFunction(
            self,
            "podcast_to_shorts_lambda",
            entry="./backend/python",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="handler",
            index="lambdas/bots/podcast_to_shorts.py",
            bundling=bundlingOptions,
            environment=environment_variables,
            layers=[face_recognition_layer, moviepy_layer],
        )

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
