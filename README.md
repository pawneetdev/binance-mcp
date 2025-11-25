# Binance MCP Server

A Model Context Protocol (MCP) server for the Binance Spot API, built using the REST-to-MCP adapter framework. This server enables Claude Desktop to interact directly with Binance's trading platform for market data, account management, and trading operations.

## Features

- Full access to Binance Spot API endpoints
- HMAC-SHA256 authenticated requests for private endpoints
- Automatic signature generation and timestamp handling
- Support for both public and authenticated endpoints
- Environment-based credential management

## Prerequisites

- Python 3.8+
- Binance API credentials (API key and secret)
- rest-to-mcp-adapter package
- Claude Desktop (for integration)

## Installation

1. Clone the repository and navigate to the project directory:
```bash
cd binance-mcp
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install python-dotenv
```

4. Set up your Binance API credentials:

Create a .env file in the project root:
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

## Configuration

### Test the Server

Before configuring Claude Desktop, test that the server runs correctly:

```bash
python run_server.py
```

You should see the server start without errors. Note the absolute paths displayed - you'll need these for Claude configuration.

### Configure Claude Desktop

1. Locate your Claude Desktop configuration file:
   - macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
   - Windows: %APPDATA%\Claude\claude_desktop_config.json

2. Add the Binance MCP server configuration:

```json
{
  "mcpServers": {
    "binance-api": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": [
        "/absolute/path/to/run_server.py"
      ]
    }
  }
}
```

Replace /absolute/path/to/ with the actual absolute paths from your system.

3. Restart Claude Desktop to activate the integration.

## Usage

Once configured, you can use Claude Desktop to interact with Binance. Example queries:

- "What is the current BTC/USDT price?"
- "Show me my account balance"
- "Get the order book for ETH/USDT"
- "Place a limit buy order for 0.01 BTC at 50000 USDT"

If credentials are not found, the server will start with NoAuth mode, which only allows access to public Binance endpoints (market data, ticker information, etc.).

## Project Structure

```
binance-mcp/
  binance_auth.py              - Binance HMAC-SHA256 authentication handler
  run_server.py                - Main MCP server entry point
  binance_spot_toolkit.json    - MCP tool definitions
  binance_spot_endpoints.json  - Canonical endpoint configurations
  .env                         - Environment variables (not committed)
  README.md                    - This file
```

## Authentication

The server uses Binance's HMAC-SHA256 signature authentication:

1. API Key: Sent in the X-MBX-APIKEY header
2. Timestamp: Automatically added to requests (current time in milliseconds)
3. Signature: HMAC-SHA256 hash of the query string, generated using your API secret

All authentication is handled automatically by the BinanceAuth class in binance_auth.py.

## Security Notes

- Never commit your .env file or expose your API credentials
- Use API key restrictions in your Binance account settings
- Limit API key permissions to only what's needed (e.g., disable withdrawals)
- Consider using IP whitelisting for additional security
- Store your configuration file securely
- Regularly rotate your API keys

## How It Works

1. Tool Registry: Loads MCP tool definitions from binance_spot_toolkit.json
2. Endpoints: Loads canonical endpoint configurations from binance_spot_endpoints.json
3. Authentication: Initializes either BinanceAuth (with credentials) or NoAuth (public only)
4. Execution: Uses APIExecutor to make authenticated requests to https://api.binance.com
5. Server: Runs the MCP server to expose tools to LLMs and agents via JSON-RPC
6. Communication: Claude Desktop communicates with the server over stdio

## Troubleshooting

- If Claude doesn't recognize the server, check that the paths in claude_desktop_config.json are absolute
- Verify your API credentials are correct in the .env file or config
- Check Claude Desktop logs for connection errors
- Ensure the virtual environment is activated when testing
- For authentication errors, verify your API key has the required permissions

## Binance API Documentation

For more information about the Binance Spot API:
- Binance API Documentation: https://binance-docs.github.io/apidocs/spot/en/
- API Key Setup: https://www.binance.com/en/support/faq/how-to-create-api-360002502072
- Security Best Practices: https://www.binance.com/en/support/faq/how-to-keep-your-account-secure-360002934791

## License

MIT License

Copyright (c) 2025 Pawneet Singh

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This project uses the REST-to-MCP adapter framework. Refer to the adapter's license for terms and conditions.
