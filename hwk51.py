from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set in .env")

client = genai.Client(api_key=api_key)
system_instruction = """
You are an experienced senior software engineer and programming mentor.
Explain technical concepts clearly, adapt your explanations to the user's level, and use practical examples when appropriate.
"""
chat = client.chats.create(
    model="gemini-3.1-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
        temperature=0.3,
    )
)

while True:
    user_input = input("\nUser: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the program.")
        break

    if user_input.lower() == "history":
        print("Conversation History:")
        for message in chat.get_history():
            role = message.role
            content = message.parts[0].text
            print(f"{role.capitalize()}: {content}")
        continue

    response = chat.send_message(user_input)

    print("AI:", response.text)
