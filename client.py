from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["math_server.py"],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )

    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    tools = await client.get_tools()
    model = ChatGroq(model="qwen/qwen3-32b")
    agent = create_agent(model, tools)

    print("MCP Client Ready!")
    print("Available tools: Math (add, multiply) and Weather")
    print("Type 'exit' or 'quit' to stop\n")

    while True:
        try:
            query = input("Enter your query: ")

            if query.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            if not query.strip():
                continue

            response = await agent.ainvoke(
                {"messages": [{"role": "user", "content": query}]}
            )

            print(f"\nResponse: {response['messages'][-1].content}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")

asyncio.run(main())