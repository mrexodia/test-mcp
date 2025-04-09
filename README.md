# Test MCP

Diagram: https://excalidraw.com/#json=bkU0xKSn3eoR36vkUYYVB,iNwcwHqD9bH7mzHj4UtZHA

MCP Clients:

- [Claude Desktop](https://claude.ai/download)
- [Cline Extension](https://cline.bot)

For development (using [uv](https://docs.astral.sh/uv/) to manage Python environments):

```sh
uv run mcp dev server.py
```

Installation (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "Test MCP": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/admin/Projects/test-mcp",
        "run",
        "server.py"
      ],
      "timeout": 600
    }
  }
}
```