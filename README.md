# Test MCP

Diagram: https://excalidraw.com/#json=uRRaOjlO8rV6Og36vjPEj,LRARtOLrhz0VdTFIxjH8Rg

## Requirements

- [uv](https://docs.astral.sh/uv) to manage the Python environment
- [nodejs](https://nodejs.org/en) for testing
- [MCP](https://modelcontextprotocol.io) clients to actually use it
  - [Claude Desktop](https://claude.ai/download)
  - [Visual Studio Code](https://vscode.dev)
    - [Cline](https://cline.bot)
    - [Roo Code](https://roocode.com)
    - [Kilo Code](https://github.com/Kilo-Org/kilocode)
  - [Jan](https://jan.ai)

**Note**: OpenRouter has many [free models](https://openrouter.ai/models?max_price=0&order=context-high-to-low) available that you can use for testing.

## Development

For testing you can run a development server and manually run tool calls:

```sh
uv run fastmcp dev
```

The fully example is implemented in `test-mcp.py`, a minimal example you can use in your own projects is in `minimal-mcp.py`.

## Installation

To install your MCP server you need to configure an [`MCP.json`](https://gofastmcp.com/integrations/mcp-json-configuration) that looks something like this:

```json
{
  "mcpServers": {
    "Test MCP": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/admin/Projects/test-mcp",
        "run",
        "test-mcp.py"
      ],
      "timeout": 600
    }
  }
}
```

For Claude Desktop there is a [detailed guide](https://modelcontextprotocol.info/docs/quickstart/user/) available.
