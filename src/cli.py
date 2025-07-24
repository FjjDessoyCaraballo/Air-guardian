#!/usr/bin/env python3
"""CLI entry points for the AirGuardian application."""

import uvicorn


def dev():
    """Run the development server with auto-reload."""
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


def start():
    """Run the production server."""
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    dev()