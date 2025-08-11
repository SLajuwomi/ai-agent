import os
import subprocess
import sys


def run_python_file(working_directory, file_path, args=[]):
    working_directory_abs_path = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file_path.startswith(working_directory_abs_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_file_path):
        return f'Error: File "{file_path}" not found.'

    if not target_file_path.endswith("py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            args=[sys.executable, target_file_path, *args],
            timeout=30,
            capture_output=True,
            cwd=working_directory_abs_path,
        )

        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"

        if result.stdout == None:
            return "No output produced"

        return f"STDOUT: {result.stdout} \n STDERR: {result.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
