import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.call_function import call_function, available_functions


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    verbose = "--verbose" in sys.argv

    client = genai.Client(api_key=api_key)

    args = sys.argv[1:]

    if args:
        user_prompt = args[0]
    else:
        print("Prompt not provided")
        print('Here is the correct usage: uv run main.py "your_prompt_goes_here"')
        print('Example: uv run main.py "How manr r\'s are in the word strawberry"')
        sys.exit(1)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    for i in range(0, 20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            if response.function_calls:
                for function_call_part in response.function_calls:
                    result = call_function(function_call_part, verbose)

                    if result.parts[0].function_response.response and verbose:
                        print(f"-> {result.parts[0].function_response.response}")

                    messages.append(
                        types.Content(
                            role="user",
                            parts=[
                                types.Part(
                                    text=result.parts[0].function_response.response[
                                        "result"
                                    ]
                                )
                            ],
                        )
                    )

                    if not result.parts[0].function_response.response:
                        raise Exception("Tool calling failed")

            for candidate in response.candidates:
                messages.append(candidate.content)

            if args and verbose:
                print("User prompt:", user_prompt)
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print(
                    "Response tokens:", response.usage_metadata.candidates_token_count
                )
            if not response.function_calls:
                print(response.text)
                break

        except Exception as e:
            return f"Error: generating response: {e}"


if __name__ == "__main__":
    main()
