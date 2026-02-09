#!/usr/bin/env python3
"""
IONOS Cloud Network Visualizer - Local Proxy Server

Part of IONOS Cloud Network Visualizer - an interactive force-directed graph
visualization of IONOS Cloud Virtual Data Center network topology.

This lightweight server does two things:
  1. Serves the ionos-cloud-network-visualizer.html frontend
  2. Proxies API requests to IONOS Cloud APIs (avoids CORS issues)

Usage:
  python3 serve.py
  python3 serve.py --port 8080

Then open http://localhost:8080 in your browser.
No pip dependencies required - uses only Python standard library.

License: Apache-2.0
"""

import http.server
import urllib.request
import urllib.parse
import urllib.error
import ssl
import json
import socket
import sys
import webbrowser
import argparse
from pathlib import Path
from typing import Optional

PORT = 8080
HTML_FILE = "ionos-cloud-network-visualizer.html"
SCRIPT_DIR = Path(__file__).parent.resolve()
MAX_PORT_RETRIES = 10
REQUEST_TIMEOUT_SECONDS = 30
MAX_RESPONSE_BYTES = 10 * 1024 * 1024  # 10 MB


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler that serves static files and proxies IONOS API calls."""

    server_port: int = PORT  # set at runtime from main()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SCRIPT_DIR), **kwargs)

    # ── Routing ──────────────────────────────────────────────────────

    def do_GET(self) -> None:
        """Route GET requests to the proxy, health endpoint, or static files."""
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/proxy":
            self._handle_proxy(parsed)
        elif parsed.path == "/health":
            self._send_json_response(200, {"status": "ok"})
        elif parsed.path in ("/", ""):
            self.path = f"/{HTML_FILE}"
            super().do_GET()
        else:
            super().do_GET()

    def do_OPTIONS(self) -> None:
        """Handle CORS preflight requests."""
        self.send_response(200)
        self._add_cors_headers()
        self.end_headers()

    # ── Proxy ────────────────────────────────────────────────────────

    def _handle_proxy(self, parsed: urllib.parse.ParseResult) -> None:
        """Forward a request to the IONOS API and relay the response."""
        params = urllib.parse.parse_qs(parsed.query)
        target_url = params.get("url", [""])[0].strip()

        if not target_url:
            self._send_json_error(400, "Missing 'url' query parameter")
            return

        # Validate URL scheme (prevent file://, gopher://, etc.)
        target_parsed = urllib.parse.urlparse(target_url)
        if target_parsed.scheme not in ("http", "https"):
            self._send_json_error(400, "Only HTTP/HTTPS URLs are allowed")
            return

        # Validate the target is an IONOS API endpoint
        target_host = (target_parsed.hostname or "").lower()
        allowed_hosts = ["api.ionos.com"]
        is_allowed = any(
            target_host == h or target_host.endswith(f".{h}")
            for h in allowed_hosts
        )
        is_ionos_regional = target_host.endswith(".ionos.com")

        if not (is_allowed or is_ionos_regional):
            self._send_json_error(
                403, f"Proxy blocked: {target_host} is not an IONOS endpoint"
            )
            return

        # Read auth token from header (never from URL)
        token = self.headers.get("X-Token", "")
        if not token:
            self._send_json_error(401, "Missing X-Token header")
            return

        # Build the upstream request
        req = urllib.request.Request(target_url, method="GET")
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", "IONOS-Cloud-Network-Visualizer/1.1")

        ctx = ssl.create_default_context()

        try:
            with urllib.request.urlopen(
                req, context=ctx, timeout=REQUEST_TIMEOUT_SECONDS
            ) as resp:
                body = resp.read(MAX_RESPONSE_BYTES + 1)
                if len(body) > MAX_RESPONSE_BYTES:
                    self._send_json_error(
                        413, f"Response exceeds {MAX_RESPONSE_BYTES // (1024*1024)} MB limit"
                    )
                    return
                self.send_response(resp.status)
                content_type = resp.headers.get("Content-Type", "application/json")
                self.send_header("Content-Type", content_type)
                self._add_cors_headers()
                self.end_headers()
                self.wfile.write(body)

        except urllib.error.HTTPError as e:
            try:
                error_body = e.read(2048).decode("utf-8", errors="replace")
            except Exception:
                error_body = "(unable to read error response)"
            self.send_response(e.code)
            self.send_header("Content-Type", "application/json")
            self._add_cors_headers()
            self.end_headers()
            self.wfile.write(
                json.dumps({
                    "error": f"IONOS API returned {e.code}",
                    "detail": error_body[:500],
                }).encode()
            )
        except urllib.error.URLError as e:
            self._send_json_error(502, f"Could not reach IONOS API: {e.reason}")
        except socket.timeout:
            self._send_json_error(504, "API request timed out")
        except OSError as e:
            self._send_json_error(502, f"Network error: {e}")

    # ── Helpers ──────────────────────────────────────────────────────

    def _send_json_response(self, code: int, data: dict) -> None:
        """Send a JSON response with the given status code."""
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self._add_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _send_json_error(self, code: int, message: str) -> None:
        """Send a JSON error response."""
        self._send_json_response(code, {"error": message})

    def _add_cors_headers(self) -> None:
        """Add CORS headers scoped to localhost origins."""
        origin = self.headers.get("Origin", "")
        if origin.startswith("http://localhost:") or origin.startswith("http://127.0.0.1:"):
            self.send_header("Access-Control-Allow-Origin", origin)
        else:
            # Fallback for direct browser access (no Origin header)
            self.send_header(
                "Access-Control-Allow-Origin",
                f"http://localhost:{ProxyHandler.server_port}",
            )
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header(
            "Access-Control-Allow-Headers", "Content-Type, X-Token, Authorization"
        )

    def log_message(self, format: str, *args) -> None:
        """Quieter logging - only show proxy requests and errors."""
        msg = format % args
        if "/proxy?" in msg or "error" in msg.lower():
            sys.stderr.write(f"  {msg}\n")


def main() -> None:
    """Start the local proxy server."""
    parser = argparse.ArgumentParser(
        description="IONOS Cloud Network Visualizer - Local Server"
    )
    parser.add_argument(
        "--port", "-p", type=int, default=PORT,
        help=f"Port to listen on (default: {PORT})",
    )
    parser.add_argument(
        "--no-browser", action="store_true",
        help="Don't auto-open the browser",
    )
    args = parser.parse_args()

    html_path = SCRIPT_DIR / HTML_FILE
    if not html_path.exists():
        print(f"ERROR: {HTML_FILE} not found in {SCRIPT_DIR}")
        print(
            "Make sure ionos-cloud-network-visualizer.html is in the same "
            "directory as this script."
        )
        sys.exit(1)

    # Auto-fallback: try requested port, then next ports if busy
    port = args.port
    server: Optional[http.server.HTTPServer] = None
    for attempt in range(MAX_PORT_RETRIES + 1):
        try:
            server = http.server.HTTPServer(("127.0.0.1", port), ProxyHandler)
            break
        except OSError:
            if attempt < MAX_PORT_RETRIES:
                print(
                    f"  Port {port} is busy, trying {port + 1}...",
                    file=sys.stderr,
                )
                port += 1
            else:
                print(
                    f"ERROR: Could not bind to any port in range "
                    f"{args.port}-{port}",
                    file=sys.stderr,
                )
                sys.exit(1)

    ProxyHandler.server_port = port
    url = f"http://localhost:{port}"

    print()
    print("  ╔═══════════════════════════════════════════════════╗")
    print("  ║     IONOS Cloud Network Visualizer                ║")
    print("  ╠═══════════════════════════════════════════════════╣")
    print(f"  ║  Running at: {url:<36} ║")
    if port != args.port:
        note = f"(port {args.port} was busy)"
        print(f"  ║  {note:<49} ║")
    print("  ║  Press Ctrl+C to stop                             ║")
    print("  ╚═══════════════════════════════════════════════════╝")
    print()

    if not args.no_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Shutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
