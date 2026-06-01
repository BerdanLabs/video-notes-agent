# MCP Adapter

`video-notes-agent` includes an optional MCP server for agents and tools that can connect to MCP
servers.

Install:

```bash
python -m pip install -e ".[mcp]"
```

Run:

```bash
video-notes-mcp
```

Example MCP server configuration:

```json
{
  "mcpServers": {
    "video-notes-agent": {
      "command": "video-notes-mcp"
    }
  }
}
```

Exposed tools:

- `create_docx_notes`: runs the full note pipeline and returns output paths plus QA/artifact metadata.
- `qa_notes`: checks a generated DOCX or Markdown file.
- `read_artifact`: reads a JSON artifact emitted by the pipeline.

The MCP adapter follows the same privacy and copyright rules as the CLI. It does not bypass DRM or
unauthorized access controls.
