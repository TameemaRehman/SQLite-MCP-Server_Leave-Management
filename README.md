# SQLite-MCP-Server_Leave-Management
# LeaveManagement MCP Server

A simple leave-management service using FastMCP and SQLite.

## Installation

1. Create and activate a Python virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows
   ```
2. Install the dependency:

   ```bash
   pip install fastmcp
   ```

## Running

Start the server:

```bash
python server.py
```

It will listen on `http://0.0.0.0:8000`.

## Basic Usage

* **List all requests**: `GET /tool/list_leaves`
* **Create request**: `POST /tool/create_leave` with JSON `{ "employee_name": "Name", "start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD", "reason": "..." }`
* **Get a request**: `GET /resource/leave://<id>`
* **Update status**: `POST /tool/update_leave` with JSON `{ "leave_id": <id>, "status": "Approved" }`
* **Delete request**: `POST /tool/delete_leave` with JSON `{ "leave_id": <id> }`

---

*Auto-generated basic README*
