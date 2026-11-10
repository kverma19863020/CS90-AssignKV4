"""Your MCP server: the same four tools, offered to any MCP host. Part 5 of HANDOUT.md.

YOU WRITE this file. It is short: about 15 lines.

What it must do:
  1. Create an MCPServer named "a4-tools" and keep it in a module-level variable named mcp.
  2. Register every function in agent.tools.TOOLS as a tool, with mcp.add_tool(fn).
     That is the same as putting @mcp.tool() on the function: the function's name becomes
     the tool's name, its docstring becomes the description, and its parameters become
     the input schema.
  3. Only when run as a program (inside `if __name__ == "__main__":`), read one required
     command-line option, --workspace PATH, call tools.use_workspace(PATH), then
     mcp.run(transport="stdio").

Importing this file must not start the server: the tests import it and talk to `mcp`
directly.
"""

import argparse

from mcp.server import MCPServer

from agent import tools

mcp = MCPServer("a4-tools")

# Each function's name, docstring and parameters become the tool's name, description
# and input schema, so an MCP host sees exactly what the local agent's model sees.
for fn in tools.TOOLS:
    mcp.add_tool(fn)


def main() -> None:
    parser = argparse.ArgumentParser(description="The a4-tools MCP server.")
    parser.add_argument("--workspace", required=True, help="the project folder the tools work in")
    args = parser.parse_args()
    tools.use_workspace(args.workspace)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
