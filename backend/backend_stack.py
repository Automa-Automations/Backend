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
        my_function = python.PythonFunction(self, "MyFunction",
            entry="./backend/python",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="lambda_handler",
            index="lambdas/hello_world.py",
            bundling=python.BundlingOptions(
                asset_excludes=[".venv"]
            )
        )
