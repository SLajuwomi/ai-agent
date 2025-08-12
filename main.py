import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt, MAX_ITERATIONS
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

    if verbose:
        print("\nUser prompt", user_prompt)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    for iterations in range(0, MAX_ITERATIONS):
        if iterations >= MAX_ITERATIONS:
            print(f"Max iterations ({MAX_ITERATIONS}) reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            return f"Error: generating response: {e}"


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    for candidate in response.candidates:
        messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        result = call_function(function_call_part, verbose)

        if result.parts[0].function_response.response and verbose:
            print(f"-> {result.parts[0].function_response.response}")

        if verbose:
            print(f"-> {result.parts[0].function_response.response}")

        function_responses.append(result.parts[0])

    if not function_responses:
        raise Exception("Tool calling failed")

    messages.append(types.Content(role="user", parts=function_responses))


if __name__ == "__main__":
    main()
