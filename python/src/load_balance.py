import socket
import threading
from typing import List

class LoadBalancer:
    def __init__(self, listen_port: int, service_addresses: List[tuple]):
        self.listen_port = listen_port
        self.service_addresses = service_addresses
        self.current = 0

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', self.listen_port))
        server.listen()
        print(f"LoadBalancer listening on port {self.listen_port}")
        while True:
            client_sock, _ = server.accept()
            threading.Thread(target=self.handle_client, args=(client_sock,)).start()

    def handle_client(self, client_sock):
        try:
            data = client_sock.recv(1024)
            # Escolhe o próximo service (round-robin)
            target_addr = self.service_addresses[self.current]
            self.current = (self.current + 1) % len(self.service_addresses)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(target_addr)
                s.sendall(data)
                response = s.recv(1024)
            client_sock.sendall(response)
        except Exception as e:
            print(f"Erro no LoadBalancer: {e}")
        finally:
            client_sock.close()


if __name__ == "__main__":
    service_addresses = [("localhost", 3001), ("localhost", 3002)]
    lb = LoadBalancer(listen_port=2000, service_addresses=service_addresses)
    lb.start()