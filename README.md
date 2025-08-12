# AI Agent Pet Project

AI agent that uses the Gemini API to use an LLM to perform function calling to safely interact with a constrained working directory (`./calculator`). The agent can:

- List files and directories inside the sandbox
- Read file contents (truncated to 10,000 chars)
- Execute Python files (only within the sandbox)
- Write / overwrite files in the sandbox

These capabilities let the model inspect, run, and iteratively modify a small project (here: a console math expression calculator) while staying inside a controlled folder.

---

## Features

- Gemini 2.0 Flash model function-calling loop (up to 20 tool-use turns)
- Secure path confinement (prevents escaping the working directory)
- Simple infix arithmetic calculator with operator precedence (`+ - * /`)
- ASCII boxed rendering of results
- Unit tests for calculator logic

---

## Project Structure

```
ai-agent/
	main.py               # Agent entrypoint
	config.py             # System prompt + constants
	functions/            # Tool implementations + schemas
		get_files_info.py
		get_file_content.py
		run_python.py
		write_file.py
		call_function.py    # Dispatch + working dir injection
	calculator/           # Sandbox the agent can explore
		main.py             # CLI wrapper for Calculator
		pkg/
			calculator.py     # Expression evaluator
			render.py         # Pretty output box
		tests.py            # Unit tests
```

---

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (recommended) or standard `pip`
- A Gemini API key (export it as `GEMINI_API_KEY`)

---

## Installation

Using uv (fast, creates an isolated environment automatically):

```bash
uv sync
```

Or with classic pip (create & activate your own virtualenv first):

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set your API key (macOS / Linux) in a `.env` file at the root of the project:

```bash
export GEMINI_API_KEY="your_key_here"
```

On Windows (PowerShell):

```powershell
$Env:GEMINI_API_KEY="your_key_here"
```

---

## Quick Start

Run an agent prompt:

```bash
uv run main.py "List the files in the project"
```

Verbose mode (shows token usage + tool call logging):

```bash
uv run main.py --verbose "Read calculator/pkg/calculator.py and explain what it does"
```

Example asking for a computation (the agent will decide to run code):

```bash
uv run main.py "Evaluate 2 * 3 - 8 / 2 + 5 using the calculator project"
```

Because the system prompt instructs the model to form a plan, it will typically:

1. List files
2. Read relevant source
3. Optionally execute `calculator/main.py "<expr>"` via `run_python_file`
4. Return the computed result

---

## Built-In Tools

| Tool               | Purpose                                                     |
| ------------------ | ----------------------------------------------------------- |
| `get_files_info`   | Enumerate files + size + dir flag in a (relative) directory |
| `get_file_content` | Read a file (safe path + size limit)                        |
| `run_python_file`  | Execute a Python file with optional arguments (timeout 30s) |
| `write_file`       | Create / overwrite a file inside the sandbox                |

All tool calls automatically inject `working_directory=./calculator` (see `functions/call_function.py`). The agent must therefore use relative paths like `pkg/calculator.py` or `main.py`.

---

## Calculator (Standalone)

You can run the calculator without the agent:

```bash
uv run calculator/main.py "3 + 5 * 2"
```

Output example:

```
┌────────────┐
│ 3 + 5 * 2  │
│            │
│ =          │
│            │
│ 13         │
└────────────┘
```

Accepted syntax: space-separated infix tokens (numbers + operators). Precedence: `*` and `/` before `+` and `-`. Parentheses are NOT implemented. Empty or whitespace expressions return `None`.

---

## Troubleshooting

- Missing key error: Ensure `GEMINI_API_KEY` is exported before running `main.py`.
- No output / repeated tool calls: The model may be iterating; it will break once no more tool calls are needed (max 20 loops).
- Path errors: Use relative paths inside the sandbox (e.g. `pkg/render.py`). Attempts to traverse outside will be rejected.
- Division: Python float division (`/`) is used; integer-looking results are rendered without decimals.

---

## Disclaimer

This is a minimal educational example and omits advanced safety controls (rate limiting, content filtering, sandboxing beyond path guard, etc.). Add those before production use.
