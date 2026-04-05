# Contributing to mcpx

Thank you for helping make mcpx better! 🎉

## Adding a New Server to the Registry

The easiest way to contribute is to add a new MCP server to the registry.

### 1. Edit `mcpx/registry.py`

Add your server entry to the `REGISTRY` dict:

```python
"my-server": {
    "description": "One sentence: what does it do?",
    "category": "developer",
    "command": "npx",
    "args": ["-y", "@myorg/mcp-server-my-server"],
    "env": {"MY_API_KEY": "<your-api-key>"},
    "requires_env": ["MY_API_KEY"],
    "requires_args": [],
    "homepage": "https://github.com/myorg/mcp-server-my-server",
    "tags": ["tag1", "tag2"],
},
```

### Categories

`search` · `web` · `browser` · `filesystem` · `memory` · `database` · `developer` · `communication` · `productivity` · `reasoning` · `utility` · `ai`

### 2. Open a Pull Request

- Fork the repo
- Add your entry
- Open a PR with the title: `[Registry] Add <server-name>`

---

## Reporting Bugs

Open an issue with:
- What command you ran
- What you expected to happen
- What actually happened
- Your OS and Python version

## Feature Requests

Open an issue describing the feature and why it would be useful.

## Development Setup

```bash
git clone https://github.com/sametdlkrn/mcpx
cd mcpx
pip install -e ".[dev]"
```

## Code Style

- Python 3.10+
- No external dependencies in the core package (stdlib only)
- `typer` and `rich` are optional extras

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
