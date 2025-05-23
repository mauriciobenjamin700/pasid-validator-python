import socket
import threading
import time

class Service:
    def __init__(self, listen_port: int, service_time: float):
        self.listen_port = listen_port
        self.service_time = service_time

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', self.listen_port))
        server.listen()
        print(f"Service listening on port {self.listen_port}")
        while True:
            client_sock, _ = server.accept()
            threading.Thread(target=self.handle_client, args=(client_sock,)).start()

    def handle_client(self, client_sock):
        data = client_sock.recv(1024)
        time.sleep(self.service_time / 1000.0)  # Simula tempo de serviço em ms
        client_sock.sendall(data)
        client_sock.close()