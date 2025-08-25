import os

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    try:
        contents = os.listdir(target_dir)
        strings = []
        strings.append(f"Result for {directory} directory:")
        for item in contents:
            item_path = os.path.join(target_dir, item)
            string = f" - {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
            strings.append(string)
        final_string = "\n".join(strings)
        return final_string
    except Exception as e:
        return f"Error: {e}"
