import os
from google.genai import types


def get_files_info(working_directory, directory="."):

    final_string = ""

    working_directory_abs_path = os.path.abspath(working_directory)
    target_directory = os.path.abspath(os.path.join(working_directory, directory))

    if not target_directory.startswith(working_directory_abs_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'

    try:
        for filename in os.listdir(target_directory):
            file_path = os.path.join(target_directory, filename)
            final_string += f"- {filename}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)} \n"
        return final_string
    except Exception as e:
        return f"Error: getting file info: {e}"
