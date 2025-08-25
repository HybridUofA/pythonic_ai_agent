import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
    if len(sys.argv) == 1:
        print("Error! No prompt provided!")
        sys.exit(1)
    prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt),)
    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt}")
        print(response.text)
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}')
        sys.exit(0)
    print(response.text)
    sys.exit(0)
if __name__ == "__main__":
    main()
