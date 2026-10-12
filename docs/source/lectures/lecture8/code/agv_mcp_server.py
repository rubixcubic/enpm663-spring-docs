"""L8 demo: a minimal MCP server with one tool, the stub AGV move.

Written for the Python mcp package 2.3.0. In mcp 2.x the class that
1.x called FastMCP is MCPServer (from mcp.server.mcpserver). The tool
wraps stub_agv.move_agv, a stand-in for ARIAC's /agvN/move action.

Run: started by agv_mcp_client.py over stdio (not run by hand).
"""

from typing import Annotated, Literal

from pydantic import Field

from mcp.server.mcpserver import MCPServer
from stub_agv import example_factory, move_agv

server = MCPServer("ariac-agv")
factory = example_factory()

Station = Literal["INSPECTION", "ASSEMBLY", "SHIPPING", "RECYCLING"]


@server.tool(name="move-agv")
def move(agv: Annotated[int, Field(ge=1, le=3)],
         station: Station) -> dict:
    """Move one AGV to a station (ARIAC /agvN/move)."""
    return move_agv(factory, agv, station)


if __name__ == "__main__":
    server.run("stdio")
