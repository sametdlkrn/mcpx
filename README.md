# mcpx — The MCP Server Package Manager

Install MCP servers in one command. No more manual JSON editing.

## Installation

```bash
pip install mcpx
```

## Usage

```bash
mcpx install brave-search
mcpx install github -e GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx
mcpx install filesystem --path ~/projects
mcpx list
mcpx search database
mcpx remove brave-search
```

mcpx auto-detects your AI clients (Claude Desktop, Cursor, Windsurf) and updates their config files safely, with a backup before every change.

## Commands

| Command | Description |
|---|---|
| `mcpx install <server>` | Install a server |
| `mcpx remove <server>` | Remove a server |
| `mcpx list` | List installed servers |
| `mcpx search [query]` | Search the registry |
| `mcpx info <server>` | Detailed server info |

## Supported Clients

- Claude Desktop (macOS, Windows, Linux)
- Cursor
- Windsurf

## Available Servers (15+)

brave-search, fetch, puppeteer, filesystem, memory, sqlite, postgres, github, gitlab, git, slack, google-maps, sequential-thinking, time, everart

## Safety

- Backup created before every config change
- No telemetry, no network calls, fully local

## License

MIT
