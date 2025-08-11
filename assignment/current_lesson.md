Run Python

If you thought allowing an LLM to write files was a bad idea...

You ain't seen nothin' yet! (praise the basilisk)

It's time to build the functionality for our Agent to run arbitrary Python code.

Now, it's worth pausing to point out the inherent security risks here. We have a few things going for us:

    We'll only allow the LLM to run code in a specific directory (the working_directory).
    We'll use a 30-second timeout to prevent it from running indefinitely.

But aside from that... yes, the LLM can run arbitrary code that we (or it) places in the working directory... so be careful. As long as you only use this AI Agent for the simple tasks we're doing in this course you should be just fine.

Do not give this program to others for them to use! It does not have all the security and safety features that a production AI agent would have. It is for learning purposes only.
Assignment

    Create a new function in your functions directory called run_python.py. Here's the signature to use:

def run_python_file(working_directory, file_path, args=[]):

    If the file_path is outside the working directory, return a string with an error:

f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    If the file_path doesn't exist, return an error string:

f'Error: File "{file_path}" not found.'

    If the file doesn't end with ".py", return an error string:

f'Error: "{file_path}" is not a Python file.'

    Use the subprocess.run function to execute the Python file and get back a "completed_process" object. Make sure to:
        Set a timeout of 30 seconds to prevent infinite execution
        Capture both stdout and stderr
        Set the working directory properly
        Pass along the additional args if provided
    Return a string with the output formatted to include:
        The stdout prefixed with STDOUT:, and stderr prefixed with STDERR:. The "completed_process" object has a stdout and stderr attribute.
        If the process exits with a non-zero code, include "Process exited with code X"
        If no output is produced, return "No output produced."
    If any exceptions occur during execution, catch them and return an error string:

f"Error: executing Python file: {e}"

    Update your tests.py file with these test cases, printing each result:
        run_python_file("calculator", "main.py") (should print the calculator's usage instructions)
        run_python_file("calculator", "main.py", ["3 + 5"]) (should run the calculator... which gives a kinda nasty rendered result)
        run_python_file("calculator", "tests.py")
        run_python_file("calculator", "../main.py") (this should return an error)
        run_python_file("calculator", "nonexistent.py") (this should return an error)

Run and submit the CLI tests.
