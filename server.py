from typing import Annotated, Dict
from pydantic import Field
from mcp.server.fastmcp import FastMCP

# The log_level is necessary for Cline to work: https://github.com/jlowin/fastmcp/issues/81
mcp = FastMCP("Test Server", log_level="ERROR")

@mcp.tool()
def say_hello(
    name: Annotated[str, Field(description="Name of the user to greet.")],
) -> str:
    """Says hello to the user."""
    return f"Hello {name}, greetings from your MCP server!"

@mcp.tool()
def get_weather(
    city: Annotated[str, Field(description="City to get weather for.")],
) -> str:
    """Gets the weather for the given city."""
    return f"The weather in {city} is sunny."

if __name__ == "__main__":
    mcp.run(transport="stdio")
