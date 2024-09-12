from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import os
import requests


class Pipeline:
    class Valves(BaseModel):
        OPENAI_API_BASE_URL: str = "https://api.openai.com/v1"
        OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")

    def __init__(self, name: str = "manifold: "):
        self.type = "manifold"
        self.name = name
        self.valves = self.Valves()
        self.pipelines = self.get_openai_models()

    async def on_startup(self):
        """Called when the server starts."""
        print(f"on_startup: {self.name}")

    async def on_shutdown(self):
        """Called when the server stops."""
        print(f"on_shutdown: {self.name}")

    async def on_valves_updated(self):
        """Called when the valves are updated."""
        print(f"on_valves_updated: {self.name}")
        self.pipelines = self.get_openai_models()

    def get_openai_models(self):
        """Retrieve a list of predefined OpenAI models."""
        predefined_model_ids = ['gpt-4', 'gpt-3.5-turbo', 'gpt-4o-2024-08-06', 'gpt-4o-mini']
        return [{'id': model_id, 'name': model_id} for model_id in predefined_model_ids]

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        """
        Main pipeline method that processes user messages through the OpenAI API.

        :param user_message: The message from the user.
        :param model_id: The ID of the model to use.
        :param messages: A list of message dictionaries.
        :param body: A dictionary containing the payload for the API request.
        :return: Either a string error message, a generator, or an iterator for streaming responses.
        """
        print(f"Executing pipe for {self.name}")

        # Log input details
        print(f"Messages: {messages}")

        headers = {
            "Authorization": f"Bearer {self.valves.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {**body, "model": model_id}
        self._clean_payload(payload)

        print(f"Payload: {payload}")

        try:
            response = requests.post(
                url=f"{self.valves.OPENAI_API_BASE_URL}/chat/completions",
                json=payload,
                headers=headers,
                stream=body.get("stream", False),
            )
            response.raise_for_status()
            return response.iter_lines() if body.get("stream") else response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return f"Error: {e}"

    @staticmethod
    def _clean_payload(payload: dict):
        """Remove unwanted keys from the payload."""
        keys_to_remove = {"user", "chat_id", "title"}
        for key in keys_to_remove:
            payload.pop(key, None)
