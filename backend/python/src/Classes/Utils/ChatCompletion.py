from typing import Dict, Literal, Union
from ollama import Client
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
        ):
        if llm_type == "ollama" and not ollama_base_url:
            raise ValueError("ollama_base_url is required for ollama")
        elif llm_type == "openai" and not api_key:
            raise ValueError("api_key is required for openai")

        self.llm_type = llm_type
        self.llm_model = llm_model
        self.api_key = api_key
        self.ollama_base_url= ollama_base_url


    def generate(self, user_message: str, system_prompt: Optional[str] = None, json_format: bool = False) -> Union[str, Dict, None]:
        """Generate a completion for a given user message"""
        if self.llm_type == "openai":
            return self._openai_generate(user_message, system_prompt, json_format=json_format)
        elif self.llm_type == "ollama":
            return self._ollama_generate(user_message, json_format=json_format)

    def _openai_generate(self, user_message: str, system_prompt: Optional[str] = None, json_format: bool = False) -> Union[str, None, Dict]:
        """Generate a completion using OpenAI"""
        logger.info(f"Model: {self.llm_model}")
        client = OpenAI(api_key=self.api_key)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})

        if json_format:
            while True:
                response = client.chat.completions.create(
                    model=self.llm_model,
                    messages=messages,
                    response_format={"type": "json_object"}
                )
                completion_message = response.choices[0].message.content
                if not completion_message:
                    logger.warning("Empty response. Trying again.")
                else:
                    try:
                        completion_mesage = json.loads(completion_message)
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

    def _ollama_generate(self, user_message: str, json_format: bool = False) -> Union[str, Dict, None]:
        """Generate a completion using Ollama"""
        ollama_client = Client(self.ollama_base_url)
        ollama_response = None
        if json_format:
            while True:
                try:
                    ollama_response = json.loads(
                        ollama_client.generate(
                            model=self.llm_model,
                            prompt=user_message,
                            format="json",
                            keep_alive="1m",
                        )["response"])
                    break
                except json.JSONDecodeError:
                    logger.info("Error parsing response. Trying again...")
        else:
            ollama_response = ollama_client.generate(
                    model=self.llm_model,
                    prompt=user_message,
                    keep_alive="1m",
                )["response"]

        logger.info(f"Ollama Response: {ollama_response}")
        return ollama_response
