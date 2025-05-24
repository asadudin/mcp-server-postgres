# MCP Server for PostgreSQL

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker Pulls](https://img.shields.io/docker/pulls/asadudin/mcp-server-postgres)](https://hub.docker.com/r/asadudin/mcp-server-postgres)

A Model Context Protocol (MCP) server implementation for PostgreSQL, providing a simple interface to interact with PostgreSQL databases through MCP.

## Features

- Execute SQL queries with parameterized inputs
- Run INSERT/UPDATE/DELETE operations
- Create new databases
- Create or update table schemas
- Debug PostgreSQL connections
- Containerized with Docker for easy deployment
- Environment-based configuration

## Prerequisites

- Python 3.8+
- PostgreSQL 10+
- Docker (optional, for containerized deployment)
- Docker Compose (optional, for development)

## Installation

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/asadudin/mcp-server-postgres.git
   cd mcp-server-postgres
   ```

2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

3. Update the `.env` file with your PostgreSQL credentials:
   ```env
   PG_HOST=postgres
   PG_PORT=5432
   PG_USER=postgres
   PG_PASSWORD=your_password
   PG_DATABASE=your_database
   HOST=0.0.0.0
   PORT=8056
   ```

4. Start the service using Docker Compose:
   ```bash
   docker-compose up -d
   ```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/asadudin/mcp-server-postgres.git
   cd mcp-server-postgres
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the example environment file and update it:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run the server:
   ```bash
   python mcp_server_postgres.py
   ```

## Usage

The MCP server provides the following endpoints:

### `sql_query`
Run a SELECT query and return results as JSON.

**Parameters:**
- `query`: SQL query string
- `params`: Optional JSON string of query parameters (list or dict)

**Example:**
```json
{
  "query": "SELECT * FROM users WHERE id = $1",
  "params": [1]
}
```

### `sql_execute`
Execute an INSERT/UPDATE/DELETE statement.

**Parameters:**
- `query`: SQL statement
- `params`: Optional JSON string of query parameters (list or dict)

**Example:**
```json
{
  "query": "INSERT INTO users (name, email) VALUES ($1, $2)",
  "params": ["John Doe", "john@example.com"]
}
```

### `create_database`
Create a new PostgreSQL database.

**Parameters:**
- `database_name`: Name of the database to create

### `create_or_update_table`
Create or update a table schema.

**Parameters:**
- `sql`: CREATE TABLE or ALTER TABLE SQL statement

### `debug_postgres_connection`
Debug the PostgreSQL connection.

## Environment Variables

| Variable      | Default     | Description                          |
|---------------|-------------|--------------------------------------|
| PG_HOST      | localhost   | PostgreSQL host                      |
| PG_PORT      | 5432        | PostgreSQL port                      |
| PG_USER      | postgres    | PostgreSQL username                  |
| PG_PASSWORD  |             | PostgreSQL password                  |
| PG_DATABASE  | postgres    | Default database name                |
| HOST         | 0.0.0.0    | Host to bind the MCP server to       |
| PORT         | 8056        | Port to run the MCP server on        |

## Development

### Running Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
pytest
```

### Building the Docker Image

```bash
docker build -t mcp-server-postgres .
```

## API Documentation

For detailed API documentation, refer to the [OpenAPI specification](docs/openapi.yaml).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastMCP](https://github.com/fastmcp/fastmcp) - The MCP server framework
- [asyncpg](https://github.com/MagicStack/asyncpg) - PostgreSQL client for Python
- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
