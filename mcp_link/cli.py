"""mcp-link - The MCP Server Package Manager CLI"""

import sys
import argparse

from mcp_link import __version__
from mcp_link.registry import REGISTRY, get_server, search_servers, list_by_category, CATEGORIES
from mcp_link.config import (
    detect_clients, get_installed, install_server, remove_server,
    build_server_entry, list_all_installed, CLIENTS,
)

RESET = "\033[0m"; BOLD = "\033[1m"; DIM = "\033[2m"
CYAN = "\033[36m"; GREEN = "\033[32m"; YELLOW = "\033[33m"; RED = "\033[31m"

def c(text, *codes): return "".join(codes) + str(text) + RESET

EMOJI_CAT = {
    "search": "🔍", "web": "🌐", "browser": "🖥️", "filesystem": "📁",
    "memory": "🧠", "database": "🗄️", "developer": "⚙️",
    "communication": "💬", "productivity": "📅", "reasoning": "🤔",
    "utility": "🔧", "ai": "🤖",
}
CLIENT_EMOJI = {"claude": "🟠", "cursor": "⬜", "windsurf": "🟢"}


def _resolve_clients(client_arg):
    if client_arg:
        if client_arg not in CLIENTS:
            print(c(f"Unknown client '{client_arg}'. Choose from: {', '.join(CLIENTS)}", RED))
            sys.exit(1)
        return [client_arg]
    detected = detect_clients()
    if not detected:
        print(c("No AI client config found.", YELLOW), "Use --client to specify one.")
        print(f"Available: {', '.join(CLIENTS)}")
        sys.exit(1)
    return detected


def _confirm(prompt):
    try:
        answer = input(f"\n  {prompt} [y/N] ").strip().lower()
        return answer in ("y", "yes")
    except (KeyboardInterrupt, EOFError):
        print(); return False


def cmd_install(args):
    info = get_server(args.server)
    if not info:
        print(c(f"\n✗ Server '{args.server}' not found.", RED))
        print(f"  Run {c('mcp-link search <query>', CYAN)} to find servers.\n")
        sys.exit(1)
    env_overrides = {}
    for e in (args.env or []):
        if "=" not in e:
            print(c(f"Invalid --env: '{e}'. Use KEY=value.", RED)); sys.exit(1)
        k, v = e.split("=", 1)
        env_overrides[k.strip()] = v.strip()
    missing_env = [k for k in info.get("requires_env", []) if k not in env_overrides]
    clients = _resolve_clients(getattr(args, "client", None))
    server_entry = build_server_entry(info, [], env_overrides)
    if getattr(args, "path", None):
        server_entry["args"] = [args.path if a == "{path}" else a for a in server_entry["args"]]
    else:
        server_entry["args"] = [a for a in server_entry["args"] if not (a.startswith("{") and a.endswith("}"))]
    cat_emoji = EMOJI_CAT.get(info["category"], "📦")
    cmd_str = f"{server_entry['command']} {' '.join(server_entry['args'])}"
    print()
    print(f"  {cat_emoji}  {c(args.server, BOLD)}  —  {info['description']}")
    print(f"     Command : {c(cmd_str, CYAN)}")
    if server_entry.get("env"):
        print(f"     Env vars: {c(', '.join(server_entry['env'].keys()), YELLOW)}")
    print(f"     Clients : {c(', '.join(clients), BOLD)}")
    if missing_env:
        print(f"\n  {c('⚠  Missing env vars:', YELLOW)} {', '.join(missing_env)}")
    if not getattr(args, "yes", False):
        if not _confirm("Proceed with installation?"):
            print("  Aborted.\n"); sys.exit(0)
    for cl in clients:
        config_path = install_server(cl, args.server, server_entry)
        print(f"  {CLIENT_EMOJI.get(cl,'•')} {c('✓', GREEN)} Installed for {c(cl, BOLD)}  →  {config_path}")
    print(f"\n{c('Done!', GREEN+BOLD)} Restart your AI client to load the server. 🎉\n")


def cmd_remove(args):
    clients = _resolve_clients(getattr(args, "client", None))
    print(f"\n  Removing {c(args.server, RED+BOLD)} from: {c(', '.join(clients), BOLD)}")
    if not getattr(args, "yes", False):
        if not _confirm("Proceed?"):
            print("  Aborted.\n"); sys.exit(0)
    any_removed = False
    for cl in clients:
        removed = remove_server(cl, args.server)
        if removed:
            print(f"  {CLIENT_EMOJI.get(cl,'•')} {c('✓', GREEN)} Removed from {c(cl, BOLD)}")
            any_removed = True
        else:
            print(f"  {CLIENT_EMOJI.get(cl,'•')} {c(f'Not installed in {cl}', DIM)}")
    if any_removed:
        print(f"\n{c('Done!', GREEN+BOLD)} Restart your AI client.\n")


def cmd_list(args):
    all_installed = list_all_installed()
    if not all_installed:
        print(f"\n{c('No MCP servers installed yet.', YELLOW)}")
        print(f"Run {c('mcp-link search', CYAN)} to discover servers.\n"); return
    target = [args.client] if getattr(args, "client", None) else list(all_installed.keys())
    print()
    for cl in target:
        servers = all_installed.get(cl, {})
        print(f"{CLIENT_EMOJI.get(cl,'•')}  {c(cl.capitalize(), BOLD+CYAN)}")
        if not servers:
            print(f"    {c('(no servers installed)', DIM)}")
        else:
            for name, cfg in servers.items():
                in_reg = c("✓", GREEN) if name in REGISTRY else c("—", DIM)
                cmd = f"{cfg.get('command','')} {' '.join(cfg.get('args',[]))}"
                print(f"    {c(name, BOLD):<30} {cmd[:55]}  [{in_reg}]")
        print()


def cmd_search(args):
    query = getattr(args, "query", None)
    category = getattr(args, "category", None)
    print()
    if query:
        results = search_servers(query)
        if not results:
            print(f"{c(f'No servers found for "{query}".', YELLOW)}\n"); return
        title = f"🔍  Results for '{query}'"
    else:
        grouped = list_by_category(category)
        results = []
        for cat_name in sorted(grouped.keys()): results.extend(grouped[cat_name])
        title = "📦  MCP Server Registry"
    print(f"{c(title, BOLD+CYAN)}\n")
    col_w = 22
    print(f"  {'NAME':<{col_w}} {'CATEGORY':<16} DESCRIPTION")
    print(f"  {'─'*col_w} {'─'*16} {'─'*38}")
    for name, info in results:
        cat = info["category"]; emoji = EMOJI_CAT.get(cat, "📦")
        print(f"  {c(name, CYAN):<{col_w+9}} {emoji} {cat:<14} {info['description'][:45]}")
    print(f"\n  {c(f'{len(results)} server(s) found.', DIM)}")
    print(f"  Install: {c('mcp-link install <name>', BOLD+CYAN)}\n")


def cmd_info(args):
    info = get_server(args.server)
    if not info:
        print(c(f"Server '{args.server}' not found.", RED)); sys.exit(1)
    install_cmd = f"mcp-link install {args.server}"
    for k in info.get("requires_env", []): install_cmd += f" -e {k}=<value>"
    print()
    print(f"  {EMOJI_CAT.get(info['category'],'📦')}  {c(args.server, BOLD+CYAN)}")
    print(f"  {info['description']}\n")
    print(f"  Command   {c(info['command'] + ' ' + ' '.join(info['args']), CYAN)}")
    print(f"  Homepage  {info['homepage']}")
    print(f"  Tags      {' '.join('#'+t for t in info['tags'])}")
    if info.get("requires_env"):
        print(f"  Env vars  {c(', '.join(info['requires_env']), YELLOW)}")
    print(f"\n  {c('Install:', BOLD)}  {c(install_cmd, BOLD+CYAN)}\n")


def cmd_version(_): print(f"mcp-link {c('v'+__version__, BOLD+CYAN)}")


def build_parser():
    parser = argparse.ArgumentParser(prog="mcp-link", description="📦  mcp-link — The MCP Server Package Manager", add_help=True)
    parser.add_argument("--version", action="version", version=f"mcp-link v{__version__}")
    sub = parser.add_subparsers(dest="command", metavar="<command>")
    p = sub.add_parser("install", help="Install an MCP server")
    p.add_argument("server"); p.add_argument("-c", "--client")
    p.add_argument("-e", "--env", action="append", metavar="KEY=VALUE")
    p.add_argument("-p", "--path"); p.add_argument("-y", "--yes", action="store_true")
    p.set_defaults(func=cmd_install)
    p = sub.add_parser("remove", help="Remove an MCP server")
    p.add_argument("server"); p.add_argument("-c", "--client"); p.add_argument("-y", "--yes", action="store_true")
    p.set_defaults(func=cmd_remove)
    p = sub.add_parser("list", help="List installed servers")
    p.add_argument("-c", "--client"); p.set_defaults(func=cmd_list)
    p = sub.add_parser("search", help="Search the registry")
    p.add_argument("query", nargs="?"); p.add_argument("-c", "--category"); p.set_defaults(func=cmd_search)
    p = sub.add_parser("info", help="Show server details")
    p.add_argument("server"); p.set_defaults(func=cmd_info)
    p = sub.add_parser("version", help="Show version"); p.set_defaults(func=cmd_version)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help(); sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
