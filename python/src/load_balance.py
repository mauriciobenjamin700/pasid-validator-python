import socket
import threading
from typing import List

from src.abstract_proxy import AbstractProxy
from src.utils import add_timestamp_to_message

class LoadBalancer(AbstractProxy):
    """
    Classe LoadBalancer que implementa um balanceador de carga simples.
    O LoadBalancer escuta em uma porta especificada e aceita conexões de clientes.
    Quando um cliente se conecta, cria uma nova thread para lidar com a conexão.
    O LoadBalancer distribui as mensagens recebidas entre os serviços disponíveis de forma round-robin.
    Se um serviço estiver ocupado, o LoadBalancer tenta o próximo serviço na lista.
    Se não houver serviços disponíveis, responde com "busy".

    Args:
        listen_port (int): A porta na qual o LoadBalancer irá escutar.
        service_addresses (List[tuple]): Lista de tuplas contendo endereços IP e portas dos serviços disponíveis.
        Cada tupla deve ser no formato (ip, port).
    Returns:
        None
    """
    def __init__(self, listen_port: int, service_addresses: List[tuple]):
        super().__init__()
        self.listen_port = listen_port
        self.service_addresses = service_addresses
        self.current = 0

    def start(self):
        """
        Método para iniciar o LoadBalancer.
        Cria um socket que escuta na porta especificada e aceita conexões de clientes.
        Quando um cliente se conecta, cria uma nova thread para lidar com a conexão.
        O LoadBalancer distribui as mensagens recebidas entre os serviços disponíveis de forma round-robin.
        Se um serviço estiver ocupado, o LoadBalancer tenta o próximo serviço na lista.
        Se não houver serviços disponíveis, responde com "busy".

        Args:
            None
        Returns:
            None
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', self.listen_port))
        server.listen()
        self.sys_log(f"LoadBalancer listening on port {self.listen_port}")
        while True:
            client_sock, _ = server.accept()
            threading.Thread(target=self.handle_client, args=(client_sock,)).start()

    def handle_client(self, client_sock: socket.socket):
        """
        Método para lidar com a conexão de um cliente.
        Recebe uma mensagem do cliente, verifica se é uma configuração de serviços.
        Se for, atualiza a lista de endereços dos serviços.
        Se não for, adiciona um timestamp à mensagem e tenta enviar para um serviço livre.
        Se um serviço estiver ocupado, tenta o próximo serviço na lista.
        Se não houver serviços disponíveis, responde com "busy".

        Args:
            client_sock (socket.socket): O socket do cliente conectado.
        Returns:
            None
        """
        try:
            data = client_sock.recv(1024).decode()
            # TODO: SE EU DESCOMENTAR ESTA LINHA, O SERVIÇO DE ORIGEM NÃO CONSEGUE ENVIAR MENSAGENS
            if data.startswith("config;"):
                # Exemplo: config;localhost:3000,localhost:3001
                self.sys_log(f"CONFIGURAÇÃO RECEBIDA: {data}")
                services = data.split(";")[1].split(",")
                self.service_addresses = [(addr.split(":")[0], int(addr.split(":")[1])) for addr in services]
                self.sys_log(f"Updated service addresses: {self.service_addresses}")
                client_sock.sendall("ok".encode())
                client_sock.close()
                return
            
            # Adiciona timestamp de chegada à mensagem
            data = add_timestamp_to_message(data)

            # Tenta encontrar um service livre (round-robin)
            for _ in range(len(self.service_addresses)):
                ip, port = self.service_addresses[self.current]
                self.current = (self.current + 1) % len(self.service_addresses)
                # Verifica se o service está livre
                if self.is_service_free(ip, port):

                    # Envia a mensagem para o service
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((ip, port))
                        s.sendall(data.encode())
                        response = s.recv(1024)
                    # Adiciona o timestamp de envio à mensagem
                    data = add_timestamp_to_message(data)
                    client_sock.sendall(response)
                    break
            else:
                # Nenhum service está livre
                client_sock.sendall("busy".encode())
        except Exception as e:
            print(f"Erro no LoadBalancer: {e}")
        finally:
            client_sock.close()


    def is_service_free(self, ip:str, port:int) -> bool:
        """
        Verifica se um serviço está livre enviando uma mensagem "ping".
        Se o serviço responder com "free", considera-o livre.
        
        Args:
            ip (str): Endereço IP do serviço.
            port (int): Porta do serviço.
        Returns:
            bool: True se o serviço estiver livre, False caso contrário.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                s.sendall("ping".encode())
                status = s.recv(1024).decode()
                return status == "free"
        except Exception:
            return False

if __name__ == "__main__":
    service_addresses = [("localhost", 3001), ("localhost", 3002)]
    lb = LoadBalancer(listen_port=2000, service_addresses=service_addresses)
    lb.start()