from loguru import logger
from functools import partial
from litellm import completion
from beartype import beartype
from beartype.typing import Dict, Optional, TypedDict, Literal, List

History = List[TypedDict('HistoryItem', {'role': Literal["user", "assistant"], 'content': str})]


class LLMClient:
    @beartype
    def predict(self, system_prompt: str, query: Union[str, History]) -> str:
        """Abstract method to be implemented by subclasses."""
        raise NotImplementedError("The 'predict' method must be implemented by subclasses.")


class OpenAIClient(LLMClient):
    @beartype
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model_name: str = "gpt-3.5-turbo-16k",
        model_params: Optional[Dict] = None,
        num_retries: int = 3
    ):
        """Initialize OpenAIClient with endpoint details and model configuration."""
        self.completion = partial(
            completion,
            model=model_name,
            num_retries=num_retries,
            api_key=api_key,
        )
        self.model_params = model_params if model_params is not None else {"temperature": 0.01}
        self.call_history = []

    @beartype
    def predict(self, system_prompt: str, query: Union[str, History]) -> str:
        """Generates a response from the LLM based on the system prompt and user query."""
        try:
            response = self.completion(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query},
                ] if isinstance(query, str) else    [{"role": "system", "content": system_prompt}] + query,
                **self.model_params,
            )
            generation = response.choices[0]["message"]["content"]
            logger.info(f"Generated response: {generation}")
            
            # Record the call history for auditing purposes
            self.call_history.append((system_prompt, query, generation))
            
            return generation
        except Exception as e:
            logger.error(f"An error occurred during completion: {e}")
            raise
