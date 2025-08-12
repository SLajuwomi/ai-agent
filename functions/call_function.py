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

    # if function_name == "get_file_content":
    #     functions_dict[function_name] = get_file_content(**args_dict)
    # if function_name == "get_files_info":
    #     functions_dict[function_name] = get_files_info(**args_dict)
    # if function_name == "run_python_file":
    #     functions_dict[function_name] = run_python_file(**args_dict)
    # if function_name == "write_file":
    #     functions_dict[function_name] = write_file(**args_dict)

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
