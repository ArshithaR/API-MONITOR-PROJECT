#!/usr/bin/env python
"""API Monitor - Main Application"""

import os
import socket


def resolve_bind_port(host, requested_port, max_attempts=10):
    """Return the first bindable port starting from the requested port."""
    for candidate in range(requested_port, requested_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((host, candidate))
                return candidate
            except OSError:
                continue
    raise OSError(f"Could not bind to ports {requested_port}-{requested_port + max_attempts - 1}")


if __name__ == "__main__":
    from app import create_app

    app = create_app()
    host = os.environ.get("HOST", "127.0.0.1")
    requested_port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "1").lower() in {"1", "true", "yes"}
    port = resolve_bind_port(host, requested_port)
    if port != requested_port:
        print(f"Requested port {requested_port} was unavailable. Using port {port} instead.")

    print("\n" + "=" * 70)
    print("API MONITOR STARTED SUCCESSFULLY")
    print("=" * 70)
    print(f"Access at: http://{host}:{port}")
    print("=" * 70 + "\n")

    app.run(debug=debug, use_reloader=False, host=host, port=port)
