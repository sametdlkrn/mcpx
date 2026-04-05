"""
Built-in MCP Server Registry.
Community can contribute new servers via Pull Requests.
"""

from typing import Optional

REGISTRY: dict[str, dict] = {
    "brave-search": {
        "description": "Web & local search via Brave Search API",
        "category": "search",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-brave-search"],
        "env": {"BRAVE_API_KEY": "<your-brave-api-key>"},
        "requires_env": ["BRAVE_API_KEY"],
        "homepage": "https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search",
        "tags": ["search", "web", "brave"],
    },
    "fetch": {
        "description": "Fetch web pages and convert to markdown",
        "category": "web",
        "command": "uvx",
        "args": ["mcp-server-fetch"],
        "env": {},
        "requires_env": [],
        "homepage": "https://github.com/modelcontextprotocol/servers/tree/main/src/fetch",
        "tags": ["fetch", "web", "http"],
    },
    "puppeteer": {
        "description": "Browser automation & screenshots via Puppeteer",
        "category": "browser",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
        "env": {},
        "requires_env": [],
        "homepage": "https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer",
        "tags": ["browser", "automation", "screenshot"],
    },
    "filesystem": {
        "description": "Read/write local files and directories",
        "category": "filesystem",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "{path}"],
        "env": {},
        "requires_env": [],
        "requires_args": ["path"],
        "homepage": "https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem",
        "tags": ["files", "filesystem", "local"],
    },
    "memory": {
        "description": "Persistent key-value memory store across sessions",
        "category": "memory",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-memory"],
        "env": {},
        "requires_env": [],
        "homepage": "https://github.com/modelcontextprotocol/servers/tree/main/src/memory",
        "tags": ["memory", "persistence", "storage"],
    },
    "sqlite": {
        "description": "Query and manage SQLite databases",
        "category": "database",
        "command": "uvx",
        "args": ["mcp-server-sqlite", "--db-path", "{db_path}"],
        "env": {},
        "requires_env": [],
        "requires_args": ["db_path"],
        "homepage": "https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite",
        "tags": ["database", "sqlite", "sql"],
    },
    "postgres": {
        "description": "Connect and query PostgreSQL databases",
        "category": "database",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-postgres", "{connection_string}"],
        "env": {},
        "requires_env": [],
        "requires_args": ["connection_string"],
        "homepage": "https://github.com/modelcontextprotocol/servers/tree/main/src/postgres",
        "tags": ["database", "postgres", "sql"],
    },
    "github": {
        "description": "GitHub repos, issues, PRs, and code search",
        "category": "developer",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "<your-github-token>"},
        "requires_env": ["GITHUB_PERSONAL_ACCESS_TOKEN"],
        "homepage": "https://github.com/modelcontextprotocol/servers/tree/main/src/github",
        "tags": ["github", "git", "code", "developer"],
    },
    "gitlab": {
        "description": "GitLab repos, issues, MRs, and pipelines",
        "category": "developer",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-gitlab"],
        "env": {"GITLAB_PERSONAL_ACCESS_TOKEN": "<your-gitlab-token>", "GITLAB_API_URL": "https://gitlab.com"},
        "requires_env": ["GITLAB_PERSONAL_ACCESS_TOKEN"],
        "homepage": "https://github.com/modelcontextprotocol/servers/tree/main/src/gitlab",
        "tags": ["gitlab", "git", "code", "developer"],
    },
    "git": {
        "description": "Git operations on local repositories",
        "category": "developer",
        "command": "uvx",
        "args": ["mcp-server-git", "--repository", "{repo_path}"],
        "env": {},
        "requires_env": [],
        "requires_args": ["repo_path"],
        "homepage": "https://github.com/modelcontextprotocol/servers/tree/main/src/git",
        "tags": ["git", "version-control", "developer"],
    },
    "slack": {
        "description": "Read and send messages, search Slack channels",
        "category": "communication",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-slack"],
        "env": {"SLACK_BOT_TOKEN": "<your-slack-bot-token>", "SLACK_TEAM_ID": "<your-team-id>"},
        "requires_env": ["SLACK_BOT_TOKEN", "SLACK_TEAM_ID"],
        "homepage": "https://github.com/modelcontextprotocol/servers/tree/main/src/slack",
        "tags": ["slack", "chat", "communication"],
    },
    "google-maps": {
        "description": "Places search, directions, and geocoding via Google Maps",
        "category": "productivity",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-google-maps"],
        "env": {"GOOGLE_MAPS_API_KEY": "<your-google-maps-key>"},
        "requires_env": ["GOOGLE_MAPS_API_KEY"],
        "homepage": "https://github.com/modelcontextprotocol/servers/tree/main/src/google-maps",
        "tags": ["maps", "location", "google"],
    },
    "sequential-thinking": {
        "description": "Structured step-by-step reasoning for complex problems",
        "category": "reasoning",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
        "env": {},
        "requires_env": [],
        "homepage": "https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking",
        "tags": ["reasoning", "thinking", "planning"],
    },
    "time": {
        "description": "Get current time and timezone conversions",
        "category": "utility",
        "command": "uvx",
        "args": ["mcp-server-time"],
        "env": {},
        "requires_env": [],
        "homepage": "https://github.com/modelcontextprotocol/servers/tree/main/src/time",
        "tags": ["time", "timezone", "utility"],
    },
    "everart": {
        "description": "AI image generation via EverArt API",
        "category": "ai",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-everart"],
        "env": {"EVERART_API_KEY": "<your-everart-key>"},
        "requires_env": ["EVERART_API_KEY"],
        "homepage": "https://github.com/modelcontextprotocol/servers/tree/main/src/everart",
        "tags": ["ai", "image", "generation"],
    },
}

CATEGORIES = sorted({v["category"] for v in REGISTRY.values()})

def get_server(name: str) -> Optional[dict]:
    return REGISTRY.get(name)

def search_servers(query: str) -> list[tuple[str, dict]]:
    query = query.lower()
    results = []
    for name, info in REGISTRY.items():
        score = 0
        if query in name: score += 3
        if query in info["description"].lower(): score += 2
        if any(query in tag for tag in info["tags"]): score += 1
        if score > 0:
            results.append((name, info, score))
    results.sort(key=lambda x: x[2], reverse=True)
    return [(name, info) for name, info, _ in results]

def list_by_category(category: Optional[str] = None) -> dict[str, list[tuple[str, dict]]]:
    grouped: dict[str, list] = {}
    for name, info in REGISTRY.items():
        cat = info["category"]
        if category and cat != category:
            continue
        grouped.setdefault(cat, []).append((name, info))
    return grouped
