"""L8 demo: the course skill tools served through MCP over stdio.

Started by skills_mcp_client.py, not by hand. Each tool is a SkillTools method;
MCP writes its input schema from the method's type hints, and the description is
the same text the orchestrator sends to Gemini. Logs go to stderr: stdout carries
the MCP messages. Written for the Python mcp package 2.3.0 (MCPServer is 1.x's FastMCP).
"""
import sys

from mcp.server.mcpserver import MCPServer

from sim_session import ros_node
from skill_tools import L8_TOOLS, SkillTools

server = MCPServer("ariac-skills")
tools = SkillTools(ros_node("skills_mcp_server"), log=lambda text: print(text, file=sys.stderr))
for decl in tools.declarations(L8_TOOLS):
    server.tool(name=decl["name"], description=decl["description"])(getattr(tools, decl["name"]))

if __name__ == "__main__":
    server.run("stdio")
