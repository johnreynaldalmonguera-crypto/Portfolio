"""
Preview the built site.

    python build.py     # once, and after every edit
    python serve.py     # then open http://localhost:8000

Standard library only.
"""

import http.server
import socketserver
import webbrowser
from functools import partial
from pathlib import Path

PORT = 8000
DIST = Path(__file__).parent / "dist"

if not (DIST / "index.html").exists():
    raise SystemExit("dist/index.html not found - run 'python build.py' first.")

handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST))
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
    webbrowser.open(f"http://localhost:{PORT}")
    print(f"Serving dist/ at http://localhost:{PORT}  (Ctrl+C to stop)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
