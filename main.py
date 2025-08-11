import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    # this is a list
    args = sys.argv[1:]

    if args:
        user_prompt = args[0]
    else:
        print("Prompt not provided")
        print("Here is the correct usage: uv run main.py \"your_prompt_goes_here\"")
        print("Example: uv run main.py \"How manr r's are in the word strawberry\"")
        sys.exit(1)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

    print(response.text)

    if args and "--verbose" in args:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
