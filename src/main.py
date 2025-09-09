#!/usr/bin/env python3
import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mcp_server.server import create_server
from config.settings import load_settings


def main():
    try:
        settings = load_settings()
        mcp = create_server(settings)
        # Only print startup message in debug mode
        if os.getenv("DEBUG", "").lower() in ("true", "1", "yes"):
            print("MCP server starting...", file=sys.stderr)
        mcp.run()
    except KeyboardInterrupt:
        if os.getenv("DEBUG", "").lower() in ("true", "1", "yes"):
            print("MCP server stopped by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Error starting MCP server: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
