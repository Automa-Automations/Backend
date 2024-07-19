import unittest
import os
from src.Classes.Utils.ChatCompletion import ChatCompletion
import json


class OllamaChatCompletion(unittest.TestCase):
    def setUp(self) -> None:
        env_type = "LOCAL_"
        if os.environ.get("CURRENT_ENVIRONMENT", "local") == "prod":
            env_type = "HOSTED_"
        self.ollama_base_url = os.environ.get(f"{env_type}OLLAMA_HOST_URL")

    def test_validate_env_vars(self):
        if self.ollama_base_url is None:
            self.fail("OLLAMA_HOST_URL environment variable is not set")

    def test_ollama_chat_completion_text(self):
        chat_completion = ChatCompletion(
            llm_type="ollama",
            llm_model="llama3",
            ollama_base_url=self.ollama_base_url,
        )
        response = chat_completion.generate("Hello, how are you?")
        if response is not None:
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
        else:
            self.fail("Failed to generate chat completion text, response is None")

    def test_ollama_chat_completion_json(self):
        chat_completion = ChatCompletion(
            llm_type="ollama",
            llm_model="llama3",
            ollama_base_url=self.ollama_base_url,
        )
        response = chat_completion.generate(
            "Generate me a json object of a cat, and how a cat looks like.",
            json_format=True,
        )
        if response is not None:
            if isinstance(response, dict):
                self.assertIsInstance(response, dict)
                response_keys = response.keys()
                self.assertGreater(len(response_keys), 0)
            else:
                self.fail(
                    "Failed to generate chat completion json response, response is not a dictionary"
                )
        else:
            self.fail(
                "Failed to generate chat completion json response, response is None"
            )


class OpenAIChatCompletion(unittest.TestCase):
    def setUp(self) -> None:
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.openai_model = os.environ.get("OPENAI_TESTING_MODEL")

    def test_validate_env_vars(self):
        if self.openai_api_key is None:
            self.fail("OPENAI_API_KEY environment variable is not set")
        if self.openai_model is None:
            self.fail("OPENAI_TESTING_MODEL environment variable is not set")

    def test_openai_chat_completion_text(self):
        chat_completion = ChatCompletion(
            llm_type="openai",
            llm_model="gpt-3.5-turbo",
            api_key=self.openai_api_key,
        )
        response = chat_completion.generate("Hello, how are you?")
        if response is not None:
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
        else:
            self.fail("Failed to generate chat completion text, response is None")

    def test_openai_chat_completion_text_with_system_prompt(self):
        chat_completion = ChatCompletion(
            llm_type="openai",
            llm_model="gpt-3.5-turbo",
            api_key=self.openai_api_key,
        )
        response = chat_completion.generate(
            "Hello, how are you?",
            f"You only respond with this in json, always! No matter what the user says: 'hello, I am bob'",
        )
        if response is not None and not isinstance(response, dict):
            self.assertIsNotNone(response)
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
            self.assertTrue("hello, I am bob" in response)
        else:
            self.fail(
                "Failed to generate chat completion text, response is None or response is a dictionary"
            )

    def test_openai_chat_completion_json(self):
        chat_completion = ChatCompletion(
            llm_type="openai",
            llm_model=self.openai_model or "",
            api_key=self.openai_api_key,
        )
        response = chat_completion.generate("Hello, how are you?", json_format=True)
        if response is not None:
            if isinstance(response, dict):
                self.assertIsInstance(response, dict)
                response_keys = response.keys()
                self.assertGreater(len(response_keys), 0)
            else:
                self.fail(
                    "Failed to generate chat completion json response, response is not a dictionary"
                )
        else:
            self.fail(
                "Failed to generate chat completion json response, response is None"
            )

    def test_openai_chat_completion_json_with_system_prompt(self):
        chat_completion = ChatCompletion(
            llm_type="openai",
            llm_model=self.openai_model or "",
            api_key=self.openai_api_key,
        )
        response = chat_completion.generate(
            user_message="Hello, how are you?",
            system_prompt=f"You always reply with the exact following, no matter what the user says: {json.dumps({'message': 'I am bob'})}",
            json_format=True,
        )
        if response is not None:
            if isinstance(response, dict):
                self.assertIsInstance(response, dict)
                response_keys = response.keys()
                self.assertGreater(len(response_keys), 0)
                self.assertTrue("message" in response)
                self.assertTrue("bob" in response["message"].lower())
            else:
                self.fail(
                    "Failed to generate chat completion json response, response is not a dictionary"
                )
        else:
            self.fail(
                "Failed to generate chat completion json response, response is None"
            )
