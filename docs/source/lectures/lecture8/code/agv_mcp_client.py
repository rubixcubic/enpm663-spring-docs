"""L8 demo: an MCP client that starts the server, lists its tools and
calls one. No LLM is involved: the client plays the part of the agent
application and makes the calls a model would ask for.

Run: python3 agv_mcp_client.py   (needs the mcp package, 2.3.0)
"""

import asyncio
import json
import sys

from mcp import Client, StdioServerParameters

SERVER = StdioServerParameters(command=sys.executable,
                               args=["agv_mcp_server.py"])
CALLS = [(1, "SHIPPING"), (1, "ASSEMBLY"), (4, "SHIPPING")]


async def main():
    async with Client(SERVER) as client:
        listing = await client.list_tools()
        for tool in listing.tools:
            print("tool:", tool.name)
            print("  description:", tool.description)
            schema = tool.input_schema
            print("  input_schema, type:", schema["type"])
            for name, rule in schema["properties"].items():
                print(f"    {name}: {json.dumps(rule)}")
            print("    required:", json.dumps(schema["required"]))
        for agv, station in CALLS:
            args = {"agv": agv, "station": station}
            result = await client.call_tool("move-agv", args)
            print("call:", json.dumps(args))
            text = result.content[0].text
            print("  is_error:", result.is_error)
            if result.is_error:
                # first line, and the reason without pydantic's tail
                lines = text.splitlines()
                print("  result:", lines[0])
                print("   ", lines[2].split("[")[0].strip())
            else:
                print("  result:", json.dumps(json.loads(text)))


asyncio.run(main())
