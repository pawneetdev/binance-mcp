"""
Binance MCP Server

MCP server for Binance Spot API integration with Claude Desktop.

MIT License
Copyright (c) 2025 Pawneet Singh
"""

from adapter import (
    APIExecutor,
    MCPServer,
    MCPTool,
    ToolRegistry,
    NoAuth
)
import json
import os
from adapter.parsing import CanonicalEndpoint
from dotenv import load_dotenv
from binance_auth import BinanceAuth
from pathlib import Path

script_dir = Path(__file__).parent.absolute()

registry_file = script_dir / "binance_spot_toolkit.json"

with open(registry_file) as f:
    data = json.load(f)

registry = ToolRegistry(name=data.get("name", "Binance Spot API"))

for tool_data in data.get("tools", []):
    tool = MCPTool(
        name=tool_data["name"],
        description=tool_data["description"],
        inputSchema=tool_data["inputSchema"],
        metadata=tool_data.get("metadata")
    )
    registry.add_tool(tool)

endpoints_file = script_dir / "binance_spot_endpoints.json"

with open(endpoints_file) as f:
    data = json.load(f)

endpoints = []

for ep_data in data:
    endpoint = CanonicalEndpoint(**ep_data)
    endpoints.append(endpoint)

load_dotenv()

# Load Binance credentials from environment variables
api_key = os.getenv("BINANCE_API_KEY", "")
api_secret = os.getenv("BINANCE_API_SECRET", "")

# If credentials are provided, use BinanceAuth; otherwise, use NoAuth for public endpoints
if api_key and api_secret:
    auth = BinanceAuth(api_key=api_key, api_secret=api_secret)
else:
    auth = NoAuth()
    print("Warning: No Binance credentials found. Only public endpoints will work.")

executor = APIExecutor(
    base_url="https://api.binance.com",
    auth=auth,
    timeout=30,
    max_retries=1
)

server = MCPServer(
    name="DataForSEO API",
    version="1.0.0",
    tool_registry=registry,
    executor=executor,
    endpoints=endpoints
)
server.run()