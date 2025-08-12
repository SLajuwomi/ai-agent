from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file
import copy
from google.genai import types


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name

    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    print(f" - Calling function: {function_name}")

    args_dict = copy.deepcopy(function_call_part.args)

    args_dict["working_directory"] = "./calculator"

    functions_dict = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    try:
        result = functions_dict[function_name](**args_dict)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": result},
                )
            ],
        )
    except KeyError:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )


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
