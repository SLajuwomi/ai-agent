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


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get content of files and output to the console. Truncate to maximum of 10,000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to get content from, relative to the working directory. This parameter is required.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute python files at the designated path with necessary arguments that the file may require, only Python files are allowed to be executed. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to write to, relative to the working directory. This parameter is required.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The OPTIONAL array of arguments that the Python file may require for execution as an array. NEVER ASK THE USER TO PROVIDE ARGUMENTS! You will determine if a particular function call you want to use needs arguments by reading the file and passing arguments based on the user's request. The user will give you plain text commands, it is up to you to determine if you can complete this task with the provided files and functions and what arguments need to be passed based on the files. This array is unpacked by the function. The parameter is NOT required and if not provided, is is set by default to an empty array by the function.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the specified content to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the Python file to execute, relative to the working directory. This parameter is required.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file as a string. This parameter is required.",
            ),
        },
    ),
)


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)
