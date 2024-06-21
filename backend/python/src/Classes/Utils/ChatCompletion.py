from typing import Literal
from ollama import Client
from typing import Optional
import json
from openai import OpenAI

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


    def generate(self, user_message: str, system_prompt: Optional[str] = None, json_format: bool = False):
        """Generate a completion for a given user message"""
        if self.llm_type == "openai":
            return self._openai_generate(user_message, system_prompt, json_format=json_format)
        elif self.llm_type == "ollama":
            return self._ollama_generate(user_message, json_format=json_format)

    def _openai_generate(self, user_message: str, system_prompt: Optional[str] = None, json_format: bool = False):
        """Generate a completion using OpenAI"""
        client = OpenAI(api_key=self.api_key)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})

        if json_format:
            response = client.chat.completions.create(
                model=self.llm_model,
                messages=messages,
                response_format={"type": "json_object"}
            )
        else:
            response = client.chat.completions.create(
                model=self.llm_model,
                messages=messages,
            )

        return response.choices[0].message.content

    def _ollama_generate(self, user_message: str, json_format: bool = False):
        """Generate a completion using Ollama"""
        llama_client = Client(self.ollama_base_url)
        if json_format:
            llama_response = json.loads(
                llama_client.generate(
                    model=self.llm_model,
                    prompt=user_message,
                    format="json",
                    keep_alive="1m",
                )["response"]
            )
        else:
            llama_response = llama_client.generate(
                    model=self.llm_model,
                    prompt=user_message,
                    keep_alive="1m",
                )

        return llama_response
