from onepiece_bot.adapters import OpenAIClient

@beartype
def chatbot(query: str, llm) -> str:
    """Simulate a chatbot interaction using the LLM, updating global history with each call."""
    global history  # Indicate that we're using the global history variable
    history.append({"role": "user", "content": query})  # Add the user query to the history

    # Generate response using the LLM with the updated history
    response = llm.predict(system_prompt=system_prompt, query=history)
    history.append({"role": "assistant", "content": response})  # Add the bot's response to the history

    return response