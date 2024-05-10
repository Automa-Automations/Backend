from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda_python_alpha as python,
    aws_lambda
    # aws_sqs as sqs,
)
from constructs import Construct

class BackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "BackendQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        stripe_payment_sheet  = python.PythonFunction(self, "stripe-payment-sheet",
            entry="./backend/python",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="handler",
            index="lambdas/stripe/payment_sheet.py",
            bundling=python.BundlingOptions(
                asset_excludes=["venv"]
            )
        )

        stripe_event_webhook  = python.PythonFunction(self, "stripe-event-webhook",
            entry="./backend/python",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="handler",
            index="lambdas/stripe/webhook.py",
            bundling=python.BundlingOptions(
                asset_excludes=["venv"]
            )
        )
