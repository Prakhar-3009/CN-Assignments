import http.server
import socketserver
import hashlib
import os
import logging
from email.utils import formatdate, parsedate_to_datetime

PORT = 8000
# Always resolve path relative to script folder
FILE_PATH = os.path.join(os.path.dirname(__file__), "cache.html")

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def generate_etag(content):
    return hashlib.md5(content).hexdigest()

def serve_file(handler):
    # Show exact file path being used
    logging.info("Looking for HTML file at: %s", os.path.abspath(FILE_PATH))

    try:
        with open(FILE_PATH, "rb") as f:
            content = f.read()
    except FileNotFoundError:
        logging.error("cache.html not found at %s", os.path.abspath(FILE_PATH))
        handler.send_error(404, "cache.html not found")
        return

    # ETag + Last-Modified
    etag = generate_etag(content)
    last_modified_time = os.path.getmtime(FILE_PATH)
    last_modified_str = formatdate(last_modified_time, usegmt=True)

    # Client headers
    if_none_match = handler.headers.get("If-None-Match")
    if_modified_since = handler.headers.get("If-Modified-Since")

    logging.info("Request for %s", handler.path)
    logging.info("If-None-Match: %s", if_none_match)
    logging.info("If-Modified-Since: %s", if_modified_since)
    logging.info("Current ETag: %s", etag)
    logging.info("Current Last-Modified: %s", last_modified_str)

    # Compare caching headers
    not_modified = False

    # Check ETag
    if if_none_match and if_none_match == etag:
        not_modified = True

    # Check Last-Modified
    if if_modified_since:
        try:
            client_time = parsedate_to_datetime(if_modified_since).timestamp()
            if int(client_time) >= int(last_modified_time):
                not_modified = True
        except Exception as e:
            logging.warning("Invalid If-Modified-Since header: %s", e)

    # Send response
    if not_modified:
        logging.info("→ File not modified, sending 304 Not Modified")
        handler.send_response(304)
        handler.send_header("ETag", etag)
        handler.send_header("Last-Modified", last_modified_str)
        handler.end_headers()
    else:
        logging.info("→ File changed or first request, sending 200 OK")
        handler.send_response(200)
        handler.send_header("Content-type", "text/html")
        handler.send_header("Content-Length", str(len(content)))
        handler.send_header("ETag", etag)
        handler.send_header("Last-Modified", last_modified_str)
        handler.end_headers()
        handler.wfile.write(content)

class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/cache.html"):
            serve_file(self)
        else:
            logging.warning("Requested unknown path: %s", self.path)
            self.send_error(404, "File not found")

# Start server
with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
    logging.info("Serving at http://localhost:%d", PORT)
    httpd.serve_forever()
