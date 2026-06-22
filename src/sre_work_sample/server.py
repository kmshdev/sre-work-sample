"""Small stdlib HTTP surface for the starter fleet."""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from sre_work_sample.runtime_fleet import build_starter_fleet


class Handler(BaseHTTPRequestHandler):
    """Serve a tiny JSON control surface for local exploration."""

    def do_GET(self) -> None:
        """Serve starter endpoints."""
        if self.path == "/health":
            self._write_json({"status": "ok", "service": "sre-work-sample"})
            return

        if self.path == "/fleet":
            fleet = build_starter_fleet()
            self._write_json(
                {
                    "runtimes": [runtime.to_dict() for runtime in fleet.runtimes],
                    "dependency": fleet.dependency.to_dict(),
                }
            )
            return

        self._write_json({"error": "not_found"}, status=404)

    def log_message(self, format: str, *args: object) -> None:
        """Keep starter output quiet unless candidates add logging."""

    def _write_json(self, payload: dict[str, object], status: int = 200) -> None:
        body = json.dumps(payload, indent=2, sort_keys=True).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> int:
    """Run the local HTTP starter service."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8080, type=int)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"serving starter control surface at http://{args.host}:{args.port}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
