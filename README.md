# my-mcp-server

[![Python](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-demo-orange)]()

A minimal FastMCP-based "Employee Tool" MCP server that demonstrates how to expose simple tools (greeting, status, and a SQL query runner) backed by PostgreSQL. This repository is intended as a small example for internal tooling, demos, or development experiments with MCP tools.

Table of Contents
- Features
- Project structure
- Requirements
- Quickstart
- Configuration
- Tools / API
- Examples
- Security & Safety
- Development & Testing
- Suggested improvements
- Contributing
- License
- Contact


## Features
- say_hello: returns a friendly greeting string.
- get_status: returns a server status string.
- run_query(query: str): executes a SQL query against a configured PostgreSQL instance and returns results (SELECT returns rows, non-SELECT returns success confirmation). Includes a basic blacklist for destructive SQL.


## Project structure
```
.gitignore            - ignored files
.python-version       - pinned Python version (>=3.13)
pyproject.toml        - project metadata & dependencies (fastmcp, mcp)
README.md             - this file
main.py               - small CLI entrypoint that prints a greeting
server.py             - FastMCP server: defines tools (say_hello, get_status, run_query)
uv.lock               - package lockfile
Output_images/        - directory for example outputs/screenshots
```

How it fits together: server.py creates a FastMCP instance named "Employee Tool" and registers three tools. The server runs using stdio transport when executed directly (mcp.run(transport="stdio")). The run_query tool uses psycopg2 to connect to PostgreSQL and run SQL statements.


## Requirements
- Python 3.13+
- PostgreSQL server for run_query tool (or adapt to another DB)
- Python dependencies declared in `pyproject.toml` (fastmcp, mcp, psycopg2 - install via pip)


## Quickstart
Follow these steps to run the server locally.

1. Clone repository

```bash
git clone https://github.com/Benaniosam-hub/Project_mcp_server_Claude.git
cd Project_mcp_server_Claude
```

2. Create and activate a virtual environment, then install the package (editable recommended for development)

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install --upgrade pip
python -m pip install -e .
```

3. Configure database credentials (recommended via environment variables; see Configuration below).

4. Run the MCP server

```bash
python server.py
```

The server will start the FastMCP instance (stdio transport). How you call the tools depends on your MCP client — for local testing you can invoke the registered tools using any MCP-compatible transport or a testing harness.


## Configuration
The current `server.py` includes placeholder PostgreSQL connection values:

- host: "localhost"
- database: "db1"
- user: "postgres"
- password: "0000"
- port: "5432"

For production or shared development, do NOT keep credentials in source control. Recommended approach:
- Export environment variables before starting the server:
  - PG_HOST, PG_DATABASE, PG_USER, PG_PASSWORD, PG_PORT
- Or update `server.py` to read from env vars (I can provide or commit this change).

Example (bash):

```bash
export PG_HOST=localhost
export PG_DATABASE=mydb
export PG_USER=postgres
export PG_PASSWORD=strongpassword
export PG_PORT=5432
```


## Tools / API (what the server exposes)
The server registers the following tools in `server.py`:

- say_hello() -> str
  - Returns: "Hello Benanio, MCP server is working."

- get_status() -> str
  - Returns: "MCP server is running successfully."

- run_query(query: str) -> list|str
  - Behavior: connects to PostgreSQL via psycopg2, blocks queries containing destructive keywords (DROP DATABASE, DROP TABLE, TRUNCATE, ALTER DATABASE). Executes the query; if it is a SELECT, returns fetched rows (as a Python list of tuples in the current implementation); otherwise commits and returns "Query executed successfully.".
  - Note: Current return format for SELECT is a list of tuples. It is recommended to convert SELECT results to a JSON-serializable list of dictionaries (column-name -> value) for better interoperability.


## Examples
Example: run a simple SELECT (conceptual - depends on MCP client transport)

- SQL: SELECT id, name FROM employees LIMIT 5;
- Current return: a Python list of tuples, e.g. [(1, 'Alice'), (2, 'Bob')]
- Recommended return format (JSON-serializable):

```json
[
  {"id": 1, "name": "Alice"},
  {"id": 2, "name": "Bob"}
]
```


## Security & Safety
- The run_query tool uses a small blacklist of destructive SQL keywords. Blacklisting is not foolproof and should not be relied upon as the only protection.
- Use the principle of least privilege: create a dedicated DB user with only the required permissions (e.g., read-only for SELECT-only usage).
- Do not commit real credentials to the repository. Use environment variables or a secrets manager.
- If exposing this server to other teams or external services, add authentication/authorization and input validation.


## Development & Testing
- Add unit tests for the tools (e.g., mock psycopg2 connections for run_query).
- Consider adding a GitHub Actions workflow to run linting and tests on PRs.
- Use an editable install (`pip install -e .`) while developing.


## Suggested improvements (next steps)
- Update `server.py` to read DB credentials from environment variables and provide clear defaults.
- Make `run_query` return JSON-serializable results with column names.
- Add logging and error handling around DB connections and query execution.
- Add tests and a CI workflow.
- Add CONTRIBUTING.md and LICENSE (MIT or another suitable license) if you plan to open source it.


## Contributing
Contributions are welcome. Suggested workflow:
1. Fork the repo
2. Create a feature branch
3. Add tests for new behavior
4. Open a Pull Request with a description of changes

Include a CONTRIBUTING.md if you want to formalize guidelines.


## License
Currently no license file is included in this repository. If you intend to make this project open-source, add a LICENSE file (for example MIT, Apache-2.0).


## Contact
If you'd like, I can:
- Commit this README (done in this change).
- Update `server.py` to read env vars and convert SELECT results to JSON-friendly output in the same commit.
- Add a basic GitHub Actions CI that runs lint and tests.

Open an issue or send a PR request with specifics and I'll help implement the next changes.
