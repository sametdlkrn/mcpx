"""
Config manager - auto-detects and updates MCP config files for:
  Claude Desktop (macOS / Windows / Linux), Cursor, Windsurf
"""

import json
import platform
import shutil
from pathlib import Path
from typing import Optional


def _claude_config_path() -> Optional[Path]:
    system = platform.system()
    if system == "Darwin":
        p = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif system == "Windows":
        p = Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    else:
        p = Path.home() / ".config" / "Claude" / "claude_desktop_config.json"
    return p


def _cursor_config_path() -> Path:
    return Path.home() / ".cursor" / "mcp.json"


def _windsurf_config_path() -> Path:
    return Path.home() / ".codeium" / "windsurf" / "mcp_config.json"


CLIENTS = {
    "claude": _claude_config_path,
    "cursor": _cursor_config_path,
    "windsurf": _windsurf_config_path,
}


def _load(path: Path) -> dict:
    if not path.exists():
        return {"mcpServers": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"mcpServers": {}}


def _save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        shutil.copy2(path, path.with_suffix(".json.bak"))
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _ensure_mcp_servers(data: dict) -> dict:
    data.setdefault("mcpServers", {})
    return data


def detect_clients() -> list[str]:
    found = []
    for name, path_fn in CLIENTS.items():
        p = path_fn()
        if p and p.exists():
            found.append(name)
    return found


def get_installed(client: str) -> dict:
    path_fn = CLIENTS.get(client)
    if not path_fn:
        return {}
    p = path_fn()
    if not p:
        return {}
    return _load(p).get("mcpServers", {})


def install_server(client: str, server_name: str, server_config: dict) -> Path:
    path_fn = CLIENTS[client]
    p = path_fn()
    data = _ensure_mcp_servers(_load(p))
    data["mcpServers"][server_name] = server_config
    _save(p, data)
    return p


def remove_server(client: str, server_name: str) -> bool:
    path_fn = CLIENTS.get(client)
    if not path_fn:
        return False
    p = path_fn()
    if not p or not p.exists():
        return False
    data = _ensure_mcp_servers(_load(p))
    if server_name not in data["mcpServers"]:
        return False
    del data["mcpServers"][server_name]
    _save(p, data)
    return True


def build_server_entry(server_info: dict, extra_args: list[str], env_overrides: dict) -> dict:
    args = list(server_info.get("args", []))
    env = dict(server_info.get("env", {}))
    env.update(env_overrides)
    entry: dict = {"command": server_info["command"], "args": args}
    if env:
        entry["env"] = env
    return entry


def list_all_installed() -> dict[str, dict[str, dict]]:
    result = {}
    for client in CLIENTS:
        installed = get_installed(client)
        if installed:
            result[client] = installed
    return result
