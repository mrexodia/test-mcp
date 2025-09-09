import argparse
from typing import Annotated
from pydantic import Field
from fastmcp import FastMCP
from urllib.parse import quote, urlparse

from helpers import *

mcp = FastMCP("Minimal MCP")

@mcp.tool()
def get_weather(
    city: Annotated[str, Field(description="City to get weather for. Do not assume the user's location, ask if unknown.")],
) -> str:
    """Gets the weather for the given city."""
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={quote(city)}&count=1&language=en&format=json"
        response = get_json(url)
        city_data = response["results"][0]
        lat = city_data["latitude"]
        lon = city_data["longitude"]
    except Exception as e:
        return f"Could not coordinates for city '{city}'\n\n{e}"

    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weather_code,temperature_2m_min,temperature_2m_max,surface_pressure_mean,relative_humidity_2m_mean&timezone=auto&current=weather_code,temperature_2m,surface_pressure,relative_humidity_2m"
        response = get_json(url)
        current = response["current"]
        code = current["weather_code"]
        current["weather_code"] = WEATHER_CODES.get(code, f"Unknown weather code: {code}")
        daily_codes = response["daily"]["weather_code"]
        for i, code in enumerate(daily_codes):
            daily_codes[i] = WEATHER_CODES.get(code, f"Unknown weather code: {code}")
        return response
    except Exception as e:
        return f"Could not get weather for city '{city}'\n\n{e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=mcp.name)
    parser.add_argument("--transport", type=str, default="stdio", help="Transport protocol to use (stdio or http://127.0.0.1:5001)")
    args = parser.parse_args()
    try:
        if args.transport == "stdio":
            mcp.run(transport="stdio")
        else:
            url = urlparse(args.transport)
            mcp.settings.host = url.hostname
            mcp.settings.port = url.port
            # NOTE: npx @modelcontextprotocol/inspector for debugging
            print(f"{mcp.name} availabile at http://{mcp.settings.host}:{mcp.settings.port}/sse")
            mcp.settings.log_level = "INFO"
            mcp.run(transport="sse")
    except KeyboardInterrupt:
        pass
