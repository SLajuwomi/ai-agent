import os

def get_files_info(working_directory, directory="."):
    if not os.path.abspath(directory).startswith(os.path.abspath(working_directory)) and directory != working_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    else:
        return "good"
