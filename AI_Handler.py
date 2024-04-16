import openai
import os
import json
import anthropic

with open('config.json') as f:
    data = json.load(f)

AI = data["ai"].lower()

if AI == "openai":
    openai.api_key = data["api"]
    openai.api_base = data["OpenAI_proxy"]


    # Config

    def load_config():

        system_messages = [
            {"role": "system", "content": data["Cirno1"]},
        ]

        return system_messages


    # Initialize Conversation History
    conversation_history_dict = {}

    # Chat GPT parameters
    PARAMS = {
        "model": "gpt-3.5-turbo",
        "max_tokens": 1000,
        "temperature": 1,
        "top_p": 0.9,
        "presence_penalty": 0.9,
        "frequency_penalty": 0.5

    }


    def get_user_conversation(user_id: str):
        return conversation_history_dict.get(user_id, [])


    def clear_user_conversation(user_id: str):
        conversation_history_dict[user_id] = load_config()


    def generate_response(user_id: str, user_input: str):
        conversation_history = get_user_conversation(user_id)

        # Initialize empty conversation history for the user if it doesn't already exist
        if not conversation_history:
            clear_user_conversation(user_id)
            conversation_history = get_user_conversation(user_id)

        # Append user input
        conversation_history.append({"role": "user", "content": user_input})

        # Restrict the conversation history to 10 messages
        conversation_history = conversation_history[-10:]

        # Create response from ChatGPT API with the updated conversation history
        response = openai.ChatCompletion.create(
            messages=conversation_history,
            api_base=openai.api_base, **PARAMS)

        # Update the conversation history for the user
        conversation_history.append({"role": "assistant", "content": response.choices[0].message.content.strip()}, )

        return response
elif AI == "claude":
    print("Anthropic API is not supported yet")
