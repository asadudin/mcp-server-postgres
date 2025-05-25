from typing import Any, Dict, Optional, Union
import asyncpg
import os
import json
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment variables
PG_HOST = os.environ.get("PG_HOST", "localhost")
PG_PORT = int(os.environ.get("PG_PORT", 5432))
PG_USER = os.environ.get("PG_USER", "postgres")
PG_PASSWORD = os.environ.get("PG_PASSWORD", "")
PG_DATABASE = os.environ.get("PG_DATABASE", "postgres")
HOST = os.environ.get("HOST", "::")
PORT = int(os.environ.get("PORT", 8054))

# Initialize FastMCP server
server = FastMCP(
    "postgres",
    host=HOST,
    port=PORT
)

# Global connection pool
pool: Optional[asyncpg.Pool] = None

async def get_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(
            host=PG_HOST,
            port=PG_PORT,
            user=PG_USER,
            password=PG_PASSWORD,
            database=PG_DATABASE,
            min_size=1,
            max_size=10,
        )
    return pool


def ensure_json_string(params: Union[str, list, dict, None]) -> Optional[str]:
    if params is None:
        return None
    if isinstance(params, str):
        return params
    # If already list or dict, convert to JSON string
    return json.dumps(params)

@server.tool()
async def sql_query(query: str, params: Optional[str] = None) -> str:
    """
    Run an arbitrary SQL query and return the results as JSON.
    Args:
        query: The SQL query string (SELECT, etc.)
        params: Optional JSON string of query parameters (list or dict)
    Returns:
        JSON string of the result rows
    """
    try:
        p = await get_pool()
        async with p.acquire() as conn:
            # params must be a JSON string (or None)
            args = json.loads(params) if params else None
            records = await conn.fetch(query, *(args or []))
            result = [dict(r) for r in records]
            return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@server.tool()
async def sql_execute(query: str, params: Optional[str] = None) -> str:
    """
    Execute an INSERT/UPDATE/DELETE SQL statement.
    Args:
        query: The SQL statement
        params: Optional JSON string of query parameters (list or dict)
    Returns:
        JSON string with number of affected rows
    """
    try:
        p = await get_pool()
        async with p.acquire() as conn:
            # params must be a JSON string (or None)
            args = json.loads(params) if params else None
            result = await conn.execute(query, *(args or []))
            return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": str(e)})

@server.tool()
async def debug_postgres_connection() -> str:
    """
    Debug the Postgres connection to help diagnose issues.
    """
    try:
        p = await get_pool()
        async with p.acquire() as conn:
            version = await conn.fetchval("SELECT version()")
            return json.dumps({"status": "ok", "postgres_version": version})
    except Exception as e:
        return json.dumps({"error": str(e)})

@server.tool()
async def create_database(database_name: str) -> str:
    """
    Create a new PostgreSQL database.
    Args:
        database_name: The name of the database to create.
    Returns:
        JSON string with the result or error.
    """
    try:
        # Connect to the default 'postgres' DB to create a new DB
        conn = await asyncpg.connect(
            host=PG_HOST,
            port=PG_PORT,
            user=PG_USER,
            password=PG_PASSWORD,
            database="postgres"
        )
        await conn.execute(f'CREATE DATABASE "{database_name}"')
        await conn.close()
        return json.dumps({"status": "ok", "message": f"Database '{database_name}' created."})
    except Exception as e:
        return json.dumps({"error": str(e)})

@server.tool()
async def create_or_update_table(sql: str) -> str:
    """
    Create or update a table in the connected database.
    Args:
        sql: The CREATE TABLE or ALTER TABLE SQL statement.
    Returns:
        JSON string with the result or error.
    """
    try:
        p = await get_pool()
        async with p.acquire() as conn:
            await conn.execute(sql)
            return json.dumps({"status": "ok", "message": "Table created or updated."})
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    # Always use sse transport
    server.run(transport="sse")
