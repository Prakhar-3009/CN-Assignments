import socket
import logging

HOST = "127.0.0.1"
PORT = 8000

user_counter = 1

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def handle_request(client_socket, client_addr):
    global user_counter
    try:
        request = client_socket.recv(1024).decode()
        logging.info("Received request from %s:\n%s", client_addr, request)

        cookie_value = None
        for line in request.split("\r\n"):
            if line.startswith("Cookie:"):
                parts = line.split(": ", 1)
                if len(parts) == 2:
                    cookie_value = parts[1].strip()
        
        if cookie_value:
            body = f"<html><body><h1>Welcome back, {cookie_value}!</h1></body></html>"
            headers = [
                "HTTP/1.1 200 OK",
                "Content-Type: text/html; charset=UTF-8",
                f"Content-Length: {len(body.encode())}"
            ]
            logging.info("Returning visitor detected: %s", cookie_value)
        else:
            user_id = f"User{user_counter}"
            user_counter += 1
            body = f"<html><body><h1>Welcome, {user_id}!</h1></body></html>"
            headers = [
                "HTTP/1.1 200 OK",
                "Content-Type: text/html; charset=UTF-8",
                f"Content-Length: {len(body.encode())}",
                f"Set-Cookie: {user_id}; HttpOnly; Path=/"
            ]
            logging.info("New visitor assigned cookie: %s", user_id)

        response = "\r\n".join(headers) + "\r\n\r\n" + body
        client_socket.sendall(response.encode())
        client_socket.close()
        logging.info("Response sent to %s\n", client_addr)

    except Exception as e:
        logging.error("Error handling request from %s: %s", client_addr, e)
        client_socket.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    logging.info("Server listening at http://%s:%d", HOST, PORT)

    try:
        while True:
            client_conn, client_addr = server_socket.accept()
            handle_request(client_conn, client_addr)
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received, shutting down server...")
        server_socket.close()
        logging.info("Server has been closed successfully.")
