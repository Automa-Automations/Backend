from typing import Literal, Union, TypeVar, Type
from ollama import Client
from typing import Optional
from pydantic import BaseModel, ValidationError
from openai import OpenAI
import logging

from errors import GenerationError, ImpossibleError

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

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
        return_type: Optional[Type[T]] = None,
    ) -> Union[str, T]:
        """
        Generate a completion for a given user message
        Parameters:
        - user_message: The user message to generate a completion for
        - system_prompt: The system prompt to use
        - return_type: The Pydantic model you want the response to be (only specify this when you want JSON returned)
        Returns the completion
        """
        if self.llm_type == "openai":
            return self._openai_generate(
                user_message, system_prompt, return_type=return_type)
            )
        elif self.llm_type == "ollama":
            return self._ollama_generate(user_message, return_type=return_type)
        else:
            raise ImpossibleError(message="Invalid LLM Type!", explanation="When class was instantiated, user was supposed to pass in valid llm_type.")

    def _openai_generate(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        return_type: Optional[Type[T]] = None,
    ) -> Union[str, T]:
        """
        Generate a completion using OpenAI
        Parameters:
        - user_message: The user message to generate a completion for
        - system_prompt: The system prompt to use
        - return_type: The Pydantic model you want the response to be (only specify this when you want JSON returned)
        Returns the completion
        """
        logger.info(f"Model: {self.llm_model}")
        client = OpenAI(api_key=self.api_key)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})

        if return_type:
            max_retries = self.max_retries
            completion_message = ""
            while max_retries:
                max_retries -= 1
                response = client.chat.completions.create(
                    model=self.llm_model,
                    messages=messages,
                    response_format={"type": "json_object"},
                )
                response_message = response.choices[0].message.content
                if not response_message:
                    logger.warning("Empty response. Trying again.")
                else:
                    try:
                        response_data = return_type.model_validate_json(completion_message)
                        return response_data
                    except:
                        logger.error("Error parsing json. Trying again.")
            raise GenerationError(message="Max retries exceeded. No response returned")
        else:
            response = client.chat.completions.create(
                model=self.llm_model,
                messages=messages,
            )
            completion_message = response.choices[0].message.content
            if not completion_message:
                raise GenerationError(message="Completion Response None.")
            logger.info(f"Completion: {completion_message}")
            return completion_message

    def _ollama_generate(
        self,
        user_message: str,
        return_type: Optional[Type[T]] = None,
    ) -> Union[str, T]:
        """
        Generate a completion using Ollama
        Parameters:
        - user_message: The user message to generate a completion for
        - return_type: The Pydantic model you want the response to be (only specify this when you want JSON returned)
        Returns the completion
        """
        ollama_client = Client(self.ollama_base_url)
        if return_type:
            max_retries = self.max_retries
            while max_retries:
                max_retries -= 1
                ollama_response = ollama_client.generate(
                    model=self.llm_model,
                    prompt=user_message,
                    format="json",
                    keep_alive="1m",
                )
                if not isinstance(ollama_response, dict) or not "response" in ollama_response or not isinstance(ollama_response["response"], str):
                    raise GenerationError(message="Ollama response does not contain 'response' key")
                try:
                    correct_type_ollama_response = return_type.model_validate_json(ollama_response["response"])
                    logger.info(f"Ollama Response: {ollama_response}")
                    return correct_type_ollama_response
                except ValidationError as e:
                    logger.error(f"Error parsing ollama response: {e}. Trying again.")
                    continue
            raise GenerationError(message="Max retries exceeded. No response returned")
        else:
            ollama_response = ollama_client.generate(
                model=self.llm_model,
                prompt=user_message,
                keep_alive="1m",
            )

            if not isinstance(ollama_response, dict) or not "response" in ollama_response or not isinstance(ollama_response["response"], str):
                raise GenerationError(message="Ollama response does not contain 'response' key")
            logger.info(f"Ollama Response: {ollama_response}")
            return ollama_response["response"]
