from typing import Dict, Literal, Union
from ollama import Client, GenerateResponse
from typing import Optional
import json
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)


class ChatCompletion:
    """A class to do chat completion using different providers"""

    def __init__(
        self,
        llm_type: Literal["openai", "ollama"] = "openai",
        llm_model: str = "gpt-4o",
        api_key: Optional[str] = None,
        ollama_base_url: Optional[str] = None,
        max_retries: Optional[int] = 3,
    ) -> None:
        if llm_type == "ollama" and not ollama_base_url:
            raise ValueError("ollama_base_url is required for ollama")
        elif llm_type == "openai" and not api_key:
            raise ValueError("api_key is required for openai")

        self.llm_type = llm_type
        self.llm_model = llm_model
        self.api_key = api_key
        self.ollama_base_url = ollama_base_url
        self.max_retries = max_retries

    def generate(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        json_format: bool = False,
    ) -> Union[str, Dict, None]:
        """
        Generate a completion for a given user message
        Parameters:
        - user_message: The user message to generate a completion for
        - system_prompt: The system prompt to use
        - json_format: Whether to return the completion in json format
        Returns the completion
        """
        if self.llm_type == "openai":
            return self._openai_generate(
                user_message, system_prompt, json_format=json_format
            )
        elif self.llm_type == "ollama":
            return self._ollama_generate(user_message, json_format=json_format)

    def _openai_generate(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        json_format: bool = False,
    ) -> Union[str, None, Dict]:
        """
        Generate a completion using OpenAI
        Parameters:
        - user_message: The user message to generate a completion for
        - system_prompt: The system prompt to use
        - json_format: Whether to return the completion in json format
        Returns the completion
        """
        logger.info(f"Model: {self.llm_model}")
        client = OpenAI(api_key=self.api_key)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})

        if json_format:
            max_retries = self.max_retries
            completion_message = ""
            while max_retries:
                max_retries -= 1
                response = client.chat.completions.create(
                    model=self.llm_model,
                    messages=messages,
                    response_format={"type": "json_object"},
                )
                completion_message = response.choices[0].message.content
                if not completion_message:
                    logger.warning("Empty response. Trying again.")
                else:
                    try:
                        completion_message = json.loads(completion_message)
                        break
                    except:
                        logger.info("Error parsing json. Trying again.")
            return completion_message
        else:
            response = client.chat.completions.create(
                model=self.llm_model,
                messages=messages,
            )
            completion_message = response.choices[0].message.content
            logger.info(f"Completion: {completion_message}")
            return completion_message

    def _ollama_generate(
        self, user_message: str, json_format: bool = False
    ) -> Union[str, Dict, None]:
        """
        Generate a completion using Ollama
        Parameters:
        - user_message: The user message to generate a completion for
        - json_format: Whether to return the completion in json format
        Returns the completion
        """
        ollama_client = Client(self.ollama_base_url)
        if json_format:
            max_retries = self.max_retries
            while max_retries:
                max_retries -= 1
                try:
                    ollama_response: GenerateResponse = json.loads(
                        json.dumps(
                            ollama_client.generate(
                                model=self.llm_model,
                                prompt=user_message,
                                format="json",
                                keep_alive="1m",
                            )
                        )
                    )
                    logger.info(f"Ollama Response: {ollama_response}")
                    return json.loads(ollama_response["response"])
                except json.JSONDecodeError:
                    logger.info("Error parsing response. Trying again...")
            logger.error("Max retries exceeded. No respone returned")
        else:
            ollama_response: GenerateResponse = json.loads(
                json.dumps(
                    ollama_client.generate(
                        model=self.llm_model,
                        prompt=user_message,
                        keep_alive="1m",
                    )
                )
            )

            logger.info(f"Ollama Response: {ollama_response}")
            return ollama_response["response"]
