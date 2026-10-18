"""L8 demo: an MCP client that starts skills_mcp_server.py, lists its tools and calls three.

No LLM is involved: the client makes the calls a model would ask for. ARIAC and the
skills server run first (run_sim_demo.sh). Written for the Python mcp package 2.3.0.
"""
import asyncio
import json
import os
import sys

from mcp import Client, StdioServerParameters

# env: pass this process's environment, so the server finds ROS (the default may drop it)
SERVER = StdioServerParameters(command=sys.executable, args=["skills_mcp_server.py"], env=dict(os.environ))
CALLS = [("read_testers", {}), ("robot2_move_home", {}), ("robot2_place_in_slot", {"agv": 4, "slot": 1})]


async def main():
    async with Client(SERVER) as client:
        listing = await client.list_tools()
        for tool in listing.tools:
            print("tool:", tool.name)
            for name, rule in tool.input_schema.get("properties", {}).items():
                print(f"    {name}: {json.dumps(rule)}")
        for name, args in CALLS:
            result = await client.call_tool(name, args)
            print(f"call: {name}({json.dumps(args)})")
            print("  is_error:", result.is_error)
            text = result.content[0].text
            # a tool's dict comes back as indented JSON: print it on one line, so the
            # listing shows both readings; an error is plain text, so show its first 3 lines
            lines = text.splitlines()[:3] if result.is_error else [json.dumps(json.loads(text))]
            for line in lines:
                print("  result:", line)


if __name__ == "__main__":
    from sim_session import prepare, ros_node, start_watchdog
    start_watchdog()
    prepare(ros_node("l8_mcp_client"))
    asyncio.run(main())
