import os
import types
from dotenv import load_dotenv
from google import genai
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_file import schema_run_python_file
from google.genai import types
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    if len(sys.argv) == 1:
        print("Error! No prompt provided!")
        sys.exit(1)
    prompt = sys.argv[1]
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file
    ]
    )
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt),)
    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt}")
        print(response.text)
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}')
        sys.exit(0)
    if len(response.function_calls) != 0:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    if len(response.function_calls) == 0:
        print(response.text)
    sys.exit(0)
if __name__ == "__main__":
    main()
