import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.proxy_request("GET")

    def do_POST(self):
        self.proxy_request("POST")

    def proxy_request(self, method):
        # Basic demonstration of a proxy that could "strip" SSL by taking HTTP requests
        # and forwarding them. In reality, SSL stripping is complex (Needs ARP spoofing + Iptables).
        # This is a placeholder logic for the "Tool".
        try:
            url = self.path
            # Here we would log the request
            print(f"Intercepted: {url}")
            
            # Forward (This is just a dummy response for the demo)
            # In a real attack, we would use requests to fetch the actual URL content
            # response = requests.get(url)
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"SSL Stripping Proxy Active - Traffic Intercepted")
        except Exception as e:
            pass

class SSLStripper:
    def __init__(self):
        self.server = None
        self.thread = None

    def start_proxy(self, port=8080):
        try:
            self.server = HTTPServer(('', port), ProxyHandler)
            self.thread = threading.Thread(target=self.server.serve_forever)
            self.thread.start()
            return f"HTTP Proxy started on port {port} (Configure browser to use this)"
        except Exception as e:
            return f"Failed to start proxy: {e}"

    def stop_proxy(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
            return "Proxy stopped."
        return "Proxy not running."
