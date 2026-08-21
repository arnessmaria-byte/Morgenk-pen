from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
class H(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        super().end_headers()
    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()
ThreadingHTTPServer(('127.0.0.1', 8766), H).serve_forever()
