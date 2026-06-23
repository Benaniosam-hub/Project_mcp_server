# server.py
from fastmcp import FastMCP
import psycopg2

# Create an MCP server instance
mcp = FastMCP("Employee Tool")

@mcp.tool()
def say_hello() -> str:
    return "Hello Benanio, MCP server is working."

@mcp.tool()
def get_status() -> str:
    return "MCP server is running successfully."

@mcp.tool()
def run_query(query:str):

    conn=psycopg2.connect(
        host="localhost",
        database="db1",
        user="postgres",
        password="0000",
        port="5432"
    )
    cursor=conn.cursor()
    

    #Safety protection
    blocked = [
        "DROP DATABASE",
        "DROP TABLE",
        "TRUNCATE",
        "ALTER DATABASE",
    ]
    for item in blocked:
        if item in query.upper():
            cursor.close()
            conn.close()

            return f"{item} is blocked."
    cursor.execute(query)

    #SELECT statements
    if query.strip().upper().startswith("SELECT"):
        rows=cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    else:
        conn.commit()
        cursor.close()
        conn.close()
        return "Query executed successfully."

if __name__ == "__main__":
    mcp.run(transport="stdio")