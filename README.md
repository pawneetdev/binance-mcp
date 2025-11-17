# Binance MCP

This repository is for building a Binance MCP server. Currently, it contains test code as I learn how to work with MCP servers, LangChain, and different transport types.

## Current Test Implementation

A demonstration of multiple FastMCP servers using different transport types, integrated with LangChain and Groq LLM.

## Features

- Two MCP servers (Math and Weather) using different transports
- Math server: stdio transport with add and multiply tools
- Weather server: streamable-http transport with weather lookup
- LangChain agent integration with Groq LLM
- Multi-server client connecting to both servers simultaneously

## Prerequisites

- Python 3.8 or higher
- Groq API key

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file with your Groq API key:

```bash
GROQ_API_KEY=your_api_key_here
```

## Running the Demo

### Start Weather Server

In terminal 1:

```bash
python weather.py
```

This starts the weather MCP server on `http://localhost:8000`.

### Run the Client

In terminal 2:

```bash
python client.py
```

The client will:
- Connect to both math (stdio) and weather (http) servers
- Use Groq's Qwen model to process queries
- Test math operations: "(3 + 5) X 12"
- Test weather lookup: "What's the weather in Delhi?"

## Project Structure

```
.
├── math_server.py       # Math MCP server (stdio)
├── weather.py           # Weather MCP server (http)
├── client.py            # LangChain multi-server client
├── main.py              # Simple hello world
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Troubleshooting

- Ensure virtual environment is activated before running scripts
- Weather server must be running before starting the client
- Check that port 8000 is available
- Verify Groq API key is set in `.env` file