# mcp-link — The MCP Server Package Manager
![mcp-link demo](demo.gif)





Install MCP servers in one command. No more manual JSON editing.


## Installation

> **Install:** `pip install mcp-link`

```bash

```


## Usage


```bash
mcp-link install brave-search
mcp-link install github -e GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx
mcp-link install filesystem --path ~/projects
mcp-link list
mcp-link search database
mcp-link remove brave-search
```


mcp-link auto-detects your AI clients (Claude Desktop, Cursor, Windsurf) and updates their config files safely, with a backup before every change.


## Commands


| Command | Description |
|---|---|
| `mcp-link install <server>` | Install a server |
| `mcp-link remove <server>` | Remove a server |
