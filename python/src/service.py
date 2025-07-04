from queue import Queue
import socket
import threading
import time

from src.abstract_proxy import AbstractProxy
from src.ia import IAService
from src.utils import add_timestamp_to_message

class Service(AbstractProxy):
    """
    Classe Service que implementa um serviço de rede simples.
    O serviço escuta em uma porta especificada e responde a mensagens de clientes.
    Quando recebe uma mensagem "ping", responde com "free" para indicar que está livre.
    Para outras mensagens, simula um tempo de serviço e envia a mensagem de volta ao cliente.
    Args:
        listen_port (int): A porta na qual o serviço irá escutar.
        service_time_ms (float): O tempo de serviço simulado em milissegundos.
    Returns:
        None
    """
    def __init__(self, listen_port: int, service_time_ms: float, max_queue_size: int = 10):
        super().__init__()
        self.listen_port = listen_port
        self.service_time_ms = service_time_ms
        self.queue = Queue()
        self.max_queue_size = max_queue_size
        self.ia_service = IAService()

    def start(self):
        """
        Inicia o serviço, criando um socket que escuta na porta especificada.
        Aceita conexões de clientes e cria uma nova thread para cada cliente.
        O serviço responde a mensagens "ping" com "free" para indicar que está livre.
        Para outras mensagens, simula um tempo de serviço e envia a mensagem de volta ao cliente.
        Args:
            None
        Returns:
            None
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', self.listen_port))
        server.listen()
        self.sys_log(f"Service listening on port {self.listen_port}")
        while True:
            # Aceita conexões de clientes
            client_sock, _ = server.accept()
            # Cria uma nova thread para lidar com o cliente
            threading.Thread(target=self.handle_client, args=(client_sock,)).start()

    def handle_client(self, client_sock: socket.socket):
        """
        Lida com a conexão de um cliente.
        Recebe uma mensagem do cliente, verifica se é um "ping" e responde com "free".
        Se a mensagem não for "ping", processa a mensagem normalmente, adiciona timestamps e simula o tempo de serviço.
        Args:
            client_sock (socket.socket): O socket do cliente conectado.
        Returns:
            None
        """
        data = client_sock.recv(1024).decode()

        self.sys_log(f"{client_sock.getsockname()} Received message: {data}")
        
        # Verifica se a mensagem é "ping"
        if data == "ping":
            if self.queue.full():
                print(f"Queue is full {self.queue.maxsize / self.max_queue_size} messages")
                client_sock.sendall("busy".encode())
            else:
                print(f"Queue is free {self.queue.maxsize / self.max_queue_size} messages")
                client_sock.sendall("free".encode())
            client_sock.close()
            return
        if self.queue.full():
            print(f"Queue is full {self.queue.maxsize / self.max_queue_size} messages")
            client_sock.sendall("busy".encode())
            client_sock.close()
            return
        self.queue.put(data)
        
        # Se não for "ping", processa a mensagem normalmente

        # Adiciona timestamp de chegada à mensagem
        data = add_timestamp_to_message(data)

        print(f"Processing message: {data}")

        
        print(
            self.ia_service.ask("Por que sistemas distribuídos são complexos?")
        )
        
        # Adiciona timestamp de envio à mensagem
        #time.sleep(3)
        data = add_timestamp_to_message(data)

        print(f"Sending message: {data}")

        # Envia a mensagem de volta ao cliente
        client_sock.sendall(data.encode())
        client_sock.close()