import os
from functions.config import config

def get_file_content(working_directory, file_path):
    target_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(target_path)
    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target_path, "r") as f:
            file_content_string = f.read(config["max_chars"])
            return file_content_string
    except Exception as e:
        return f'Error: {e}'
