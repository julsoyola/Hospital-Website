import socket

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Maximum number of queued connections

    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_socket.sendall(b"Hello, client! You are connected to the server.")
        client_socket.close()

if __name__ == "__main__":
    host = "localhost"  # Use "0.0.0.0" to listen on all available network interfaces
    port = 8888  # Choose any available port number

    start_server(host, port)
