# import asyncio
# from fastmcp import Client

# client = Client("http://localhost:8000/mcp")

# async def call_tool(a: int, b:int):
#     async with client:
#         result = await client.call_tool("add", {"a": a, "b": b})
#         print(result)

# asyncio.run(call_tool(2,5))
# asyncio.run(call_tool(10,2))

from langchain_mcp_adapters.client import MultiServerMCPClient
# from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

import asyncio

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

    import os
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    tools = await client.get_tools()
    model = ChatGroq(model="qwen/qwen3-32b")

    agent = create_agent(model, tools)

    math_response = await agent.ainvoke(
        { "messages": [{"role": "user", "content": "What's (3 + 5) X 12?"}] }
    )

    print("Math response:", math_response["messages"][-1].content)

    weather_response = await agent.ainvoke(
        { "messages": [{"role": "user", "content": "What's the weather in Delhi?"}] }
    )

    print("Weather response:", weather_response["messages"][-1].content)

asyncio.run(main())