# server.py
import sqlite3
from fastmcp import FastMCP
from typing import List, Dict, Optional

# Initialize MCP server
mcp = FastMCP("LeaveManagement")

# Initialize SQLite connection
tmp_db = "leave_management.db"
conn = sqlite3.connect(tmp_db, check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Create the leave_requests table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS leave_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_name TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    reason TEXT,
    status TEXT DEFAULT 'Pending'
)
""")
conn.commit()

# Insert mock data if table is empty
cursor.execute("SELECT COUNT(*) AS count FROM leave_requests")
if cursor.fetchone()["count"] == 0:
    mock_leaves = [
        ('Alice Smith', '2025-06-01', '2025-06-05', 'Vacation', 'Approved'),
        ('Bob Johnson', '2025-06-10', '2025-06-12', 'Medical', 'Pending'),
        ('Carol White', '2025-06-15', '2025-06-16', 'Personal', 'Rejected'),
        ('David Brown', '2025-06-20', '2025-06-22', 'Conference', 'Pending')
    ]
    cursor.executemany(
        "INSERT INTO leave_requests (employee_name, start_date, end_date, reason, status) VALUES (?, ?, ?, ?, ?)",
        mock_leaves
    )
    conn.commit()

# === MCP tools ===
@mcp.tool()
def create_leave(employee_name: str, start_date: str, end_date: str, reason: Optional[str] = None) -> int:
    """Create a new leave request and return its ID"""
    cursor.execute(
        "INSERT INTO leave_requests (employee_name, start_date, end_date, reason) VALUES (?, ?, ?, ?)",
        (employee_name, start_date, end_date, reason)
    )
    conn.commit()
    return cursor.lastrowid

@mcp.tool()
def get_leave(leave_id: int) -> Dict:
    """Retrieve a leave request by its ID"""
    cursor.execute("SELECT * FROM leave_requests WHERE id = ?", (leave_id,))
    row = cursor.fetchone()
    return dict(row) if row else {}

@mcp.tool()
def update_leave(leave_id: int, status: str) -> bool:
    """Update the status of an existing leave request"""
    cursor.execute("UPDATE leave_requests SET status = ? WHERE id = ?", (status, leave_id))
    conn.commit()
    return cursor.rowcount > 0

@mcp.tool()
def delete_leave(leave_id: int) -> bool:
    """Delete a leave request by its ID"""
    cursor.execute("DELETE FROM leave_requests WHERE id = ?", (leave_id,))
    conn.commit()
    return cursor.rowcount > 0

@mcp.tool()
def list_leaves() -> List[Dict]:
    """List all leave requests"""
    cursor.execute("SELECT * FROM leave_requests")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

# Dynamic resource for individual leave requests
@mcp.resource("leave://{leave_id}")
def leave_resource(leave_id: int) -> Dict:
    """Fetch leave details via a URI resource"""
    return get_leave(leave_id)

if __name__ == "__main__":
    mcp.run()
