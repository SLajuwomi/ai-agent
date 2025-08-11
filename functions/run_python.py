import os

def run_python_file(working_directory, file_path, args=[]):
    working_directory_abs_path = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file_path.startswith(working_directory_abs_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
