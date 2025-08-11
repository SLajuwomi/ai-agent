import os

def write_file(working_directory, file_path, content):
    working_directory_abs_path = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file_path.startswith(working_directory_abs_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        if not os.path.exists(working_directory_abs_path):
            os.makedirs(working_directory_abs_path)

        with open(target_file_path, "w") as f:
            f.write(content)
            return (
                f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            )
    except Exception as e:
        return (
            f'Error: Error creating file: {e}'
        )
