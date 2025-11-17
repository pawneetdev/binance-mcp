# MCP Server Project

A FastMCP server implementation with Python client.

## Prerequisites

- Python 3.8 or higher
- uv package manager

## Setup Instructions

### 1. Create and Activate Virtual Environment

First, create a virtual environment for the project:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

Install the required packages using uv:

```bash
uv add -r requirements
```

## Running the Project

### Start the MCP Server

Run the FastMCP server on port 8000:

```bash
fastmcp run math_server.py:mcp --transport http --port 8000
```

The server will start and listen for incoming connections on `http://localhost:8000`.

### Run the Client

In a separate terminal (with the virtual environment activated), run the client:

```bash
python math_client.py
```

## Project Structure

```
.
├── math_server.py       # MCP server implementation
├── math_client.py       # Client to interact with the server
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Troubleshooting

- Make sure the virtual environment is activated before installing dependencies or running scripts
- Ensure the server is running before starting the client
- Check that port 8000 is not already in use by another application