import random
import argparse
from typing import Annotated
from pydantic import Field, BaseModel
from mcp.server.fastmcp import FastMCP
from urllib.parse import quote, urlparse

from helpers import *

# The log_level is necessary for Cline to work: https://github.com/jlowin/fastmcp/issues/81
mcp = FastMCP("Test MCP", log_level="ERROR")

@mcp.tool()
def say_hello(
    name: Annotated[str, Field(description="Name of the user to greet.")],
) -> str:
    """Says hello to the user."""
    notification(f"Hello {name}!", f"Greetings from your MCP server.")
    return f"success"

@mcp.tool()
def cat_fact() -> str:
    """Gets a random cat fact."""
    try:
        return get_json("https://catfact.ninja/fact")["fact"]
    except Exception as e:
        return f"Could not get cat fact\n\n{e}"

book_cache = []

@mcp.tool()
def suggest_book() -> str:
    """Suggests a book to read."""
    try:
        global book_cache
        if len(book_cache) == 0:
            books = get_json("https://gutendex.com/books")
            results = books["results"]
            book_cache = results
        random_book = random.choice(book_cache)
        title = random_book["title"]
        summary = random_book.get("summaries", [""])[0]
        author = random_book["authors"][0]["name"]
        return f"Here's a book you might like:\n\nTitle: {title}\nAuthor: {author}\nSummary: {summary}"
    except Exception as e:
        return f"Could not get book suggestion\n\n{e}"

@mcp.tool()
def tell_joke() -> str:
    """Tells a joke."""
    try:
        joke = get_json("https://icanhazdadjoke.com/")
        return joke["joke"]
    except Exception as e:
        return f"Could not get joke\n\n{e}"

@mcp.tool()
def find_inspiration() -> str:
    """Gets a random inspirational quote."""
    try:
        response = get_json("https://zenquotes.io/api/random")[0]
        quote = response["q"]
        author = response["a"]
        return f"{quote}\n- {author}"
    except Exception as e:
        return f"Could not get inspiration\n\n{e}"

@mcp.tool()
def get_weather(
    city: Annotated[str, Field(description="City to get weather for.")],
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
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code&forecast_days=1"
        response = get_json(url)
        current = response["current"]
        temperature_c = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        weather_code = current["weather_code"]
        weather_description = WEATHER_CODES.get(weather_code, "Unknown weather code")
        return f"{city}\n{weather_description}\nTemperature: {temperature_c}°C\nHumidity: {humidity}%."
    except Exception as e:
        return f"Could not get weather for city '{city}'\n\n{e}"

class EmailMetadata(BaseModel):
    uuid: str
    subject: str
    sender: str
    date: str

@mcp.tool()
def list_emails() -> list[EmailMetadata]:
    """Gets the latest email metadata."""
    return [{
        "uuid": email["uuid"],
        "subject": email["subject"],
        "sender": email["sender_name"],
        "date": email["date"],
    } for email in EMAILS]

@mcp.tool()
def get_email_body(
    uuid: Annotated[str, Field(description="UUID of the email to get the body for (returned by list_emails).")],
) -> str:
    """Gets the body of the email with the given UUID."""
    for email in EMAILS:
        if email["uuid"] == uuid:
            return email["body"]
    return f"ERROR: Email {uuid} not found."

@mcp.tool()
def reply_email(
    uuid: Annotated[str, Field(description="UUID of the email to get the body for (returned by list_emails).")],
    body: Annotated[str, Field(description="Text to put in the reply email.")],
) -> str:
    """Replies to the email with the given UUID with the given body."""
    for email in EMAILS:
        if email["uuid"] == uuid:
            destination = email["sender_email"]
            notification("Email sent!", f"Sent reply to {destination}!")
            return f"Successfully replied to {destination}"
    return f"ERROR: Email {uuid} not found."

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
