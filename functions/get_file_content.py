import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    working_directory_abs_path = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(working_directory_abs_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if os.path.getsize(target_file) > MAX_CHARS:
                return file_content_string + "\n" + f'[...File "{file_path}" truncated at 10000 characters]'
            
            return file_content_string
    except Exception as e:
        return f"Error: Error getting file content: {e}"
