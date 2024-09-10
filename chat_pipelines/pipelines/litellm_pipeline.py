from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv
load_dotenv()
import os
from onepiece_bot.api import chatbot
from openwebui_utils import get_last_user_message, get_last_assistant_message


class Pipeline:
    class Valves(BaseModel):
        OPENAI_API_KEY: str = ""
        pass

    def __init__(self):
        # Optionally, you can set the id and name of the pipeline.
        # Best practice is to not specify the id so that it can be automatically inferred from the filename, so that users can install multiple versions of the same pipeline.
        # The identifier must be unique across all pipelines.
        # The identifier must be an alphanumeric string that can include underscores or hyphens. It cannot contain spaces, special characters, slashes, or backslashes.
        # self.id = "openai_pipeline"
        self.name = "litellm Pipeline"
        self.valves = self.Valves(
            **{
                "OPENAI_API_KEY": os.getenv(
                    "OPENAI_API_KEY", "keys"
                ),
   	
        )
        pass

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom pipelines like RAG.
        print(f"pipe:{__name__}")

        print(messages)
        print(user_message)

        OPENAI_API_KEY = self.valves.OPENAI_API_KEY
        MODEL = "gpt-3.5-turbo"

        user_message = get_last_user_message(messages)


        try:
    	    llm = OpenAIClient(api_key=OPENAI_API_KEY ,model_name=MODEL , model_params={"temperature": 0.7})
	    response = chatbot(user_message , llm)
	    retrun response
        except Exception as e:
            return f"Error: {e}"