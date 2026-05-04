# MCP server - 1

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math") # Name of the MCP, can be anything

# Tool in mcp server
@mcp.tool()
def add(a: int, b: int) -> int:
    """__summary__
    Add two numbers
    """
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


if __name__ == "__main__":
    mcp.run(transport="stdio") 

    # This transport="stdio" argument tells the server to : 
    # use standard i/o (stdin & stdout) to receive & respond to tool fun calls

    # It will run as I/O : python mathserver.py  