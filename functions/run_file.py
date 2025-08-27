import os
import subprocess
import google.genai.types as types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs Python files, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python file to execute.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Individual argument to pass to the Python file.",
                ),
                description='The arguments for the Python file to run (e.g. "3 + 5" for calculator.py)',
            )
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    target_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(target_path)
    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(["python", file_path] + args, capture_output=True, timeout=30, text=True, cwd=working_directory)
        output = []
        if result.stdout.strip():
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr.strip():
            output.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if output:
            return "\n".join(output)
        else:
            return "No output produced."
         
                
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
