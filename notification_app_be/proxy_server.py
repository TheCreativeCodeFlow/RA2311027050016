"""Backend proxy server for Campus Notification System."""

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")

API_TOKEN = os.getenv("API_TOKEN")
EXTERNAL_API_URL = os.getenv("REACT_APP_API_URL", "http://20.207.122.201/evaluation-service/notifications")


class ProxyHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[PROXY] {args[0]}")

    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/api/notifications":
            self.handle_notifications(parsed.query)
        else:
            self.send_error(404, "Not Found")

    def handle_notifications(self, query_string: str):
        params = parse_qs(query_string)
        
        page = params.get("page", ["1"])[0]
        limit = params.get("limit", ["10"])[0]
        notification_type = params.get("notification_type", [""])[0]
        
        external_params = {
            "page": page,
            "limit": limit,
        }
        if notification_type and notification_type != "all":
            external_params["notification_type"] = notification_type
        
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json",
        }
        
        try:
            response = requests.get(
                EXTERNAL_API_URL,
                params=external_params,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(response.content)
            
        except requests.RequestException as e:
            self.send_error(502, f"Bad Gateway: {str(e)}")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")


def run_server(port: int = 5001):
    server_address = ("", port)
    httpd = HTTPServer(server_address, ProxyHandler)
    print(f"[PROXY] Server running on http://localhost:{port}")
    print(f"[PROXY] Forwarding to {EXTERNAL_API_URL}")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()