"""Simple pipeline -chatbot  onepiece ."""

import os
from typing import List, Union
from pydantic import BaseModel
from onepiece_bot.api import chatbot
from onepiece_bot.adapters import OpenAIClient


class Pipeline:
    def __init__(self):
        """
        Initialize the pipeline with configuration settings from environment variables.
        """
        self.name = "litellm Pipeline OnePiece"
        self.valves = self.Valves(OPENAI_API_KEY=os.getenv("OPENAI_API_KEY", "keys"))

    class Valves(BaseModel):
        """
        Configuration settings for the pipeline, including API keys.
        """

        OPENAI_API_KEY: str

    async def on_startup(self):
        """
        Actions to perform when the server starts.
        """
        print(f"Pipeline starting: {self.name}")

    async def on_shutdown(self):
        """
        Actions to perform when the server stops.
        """
        print(f"Pipeline stopping: {self.name}")

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, None]:
        """
        Process a pipeline request using the provided messages and model.

        Args:
            user_message (str): The user's message.
            model_id (str): The identifier for the model to use.
            messages (List[dict]): A list of message dictionaries.
            body (dict): Additional request body parameters.

        Returns:
            Union[str, None]: The response from the chatbot or an error message.
        """
        print(f"Processing request with model: {model_id}")
        print("Messages:", messages)

        api_key = self.valves.OPENAI_API_KEY
        model_name = "gpt-3.5-turbo"

        try:
            # Initialize the LLM client
            llm_client = OpenAIClient(
                api_key=api_key,
                model_name=model_name,
                model_params={"temperature": 0.7},
            )

            # Get the response from the chatbot
            response = chatbot(messages, llm_client)

            return response
        except Exception as e:
            # Handle exceptions and provide error feedback
            print(f"An error occurred: {e}")
            return f"Error: {e}"
