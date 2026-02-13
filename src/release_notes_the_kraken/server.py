import asyncio
import os
import signal

from dotenv import load_dotenv  # type: ignore
from mcp.server import Server
from mcp.server.stdio import stdio_server

from .tools import register_tools

load_dotenv()

# Initialize MCP server
server = Server("release-notes-the-kraken")

register_tools(server)


async def main():
    """Main entry point for the MCP server."""
    try:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream, write_stream, server.create_initialization_options()
            )
    except asyncio.CancelledError:
        return


def _shutdown_now(signum: int, frame: object | None) -> None:
    """Immediately terminate the process in response to a shutdown signal."""
    del signum, frame
    print("\nShutting down Release Notes The Kraken MCP server.")
    os._exit(0)


def _install_signal_handlers() -> None:
    """Register process-level signal handlers for graceful shutdown.

    Installs `_shutdown_now` as the handler for `SIGINT` and `SIGTERM`, so the
    application can terminate cleanly when interrupted (for example, via Ctrl+C)
    or when asked to stop by the operating system.
    """
    signal.signal(signal.SIGINT, _shutdown_now)
    signal.signal(signal.SIGTERM, _shutdown_now)


if __name__ == "__main__":
    _install_signal_handlers()

    print("Starting Release Notes The Kraken MCP server...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        _shutdown_now(signal.SIGINT, None)
