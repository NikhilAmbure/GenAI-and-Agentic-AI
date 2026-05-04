# Another third party tool (Weather API)
# MCP server - 2

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """
        Get the current weather for a given location.
    """
    return "It's always rainy in Cali"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

    # It will run as an API : python weather.py