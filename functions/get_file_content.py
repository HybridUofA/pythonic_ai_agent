import os
from config import MAX_CHARS
import google.genai.types as types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the file content from a given file, constrained to the max character limit of {MAX_CHARS}, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file in question. Limited by working directory.",
            )
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    target_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(target_path)
    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            return file_content_string
    except Exception as e:
        return f'Error: {e}'
