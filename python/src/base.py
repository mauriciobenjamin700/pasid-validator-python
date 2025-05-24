import socket
from typing import Optional

class AbstractProxy:
    """
    Classe abstrata que define a interface para um proxy de comunicação.
    Esta classe é responsável por enviar e receber mensagens através de sockets,
    além de registrar logs das operações realizadas.

    Args:
        log_file (Optional[str]): Caminho do arquivo de log. Se não for fornecido, usa "log.txt".
    Returns:
        None
    """
    def __init__(self, log_file: Optional[str] = None):
        self.log_file = log_file or "log.txt"
        self.init_log_file()

    def init_log_file(self):
        """
        Inicializa o arquivo de log, criando-o se não existir ou limpando seu conteúdo.
        Se o arquivo já existir, ele será sobrescrito.
        
        Args:
            None
        Returns:
            None
        """
        with open(self.log_file, 'w') as f:
            f.write("")

    def log(self, message: str):
        """
        Registra uma mensagem no log e no console.
        Esta função imprime a mensagem no console e a escreve no arquivo de log.

        Args:
            message (str): A mensagem a ser registrada.
        Returns:
            None
        """
        print(message)
        with open(self.log_file, 'a') as f:
            f.write(message + "\n")

    def send(self, ip: str, port: int, msg: str) -> None:
        """
        Método para enviar uma mensagem para um endereço IP e porta específicos.
        Este método cria um socket, conecta-se ao endereço especificado e envia a mensagem.
        Args:
            ip (str): Endereço IP do destino.
            port (int): Porta do destino.
            msg (str): Mensagem a ser enviada.
        Returns:
            None
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                s.sendall(msg.encode())
        except Exception as e:
            self.log(f"Erro ao enviar mensagem: {e}")

    def send_and_receive(self, ip: str, port: int, msg: str) -> str:
        """
        Método para enviar uma mensagem e receber uma resposta do servidor.
        Este método cria um socket, conecta-se ao endereço especificado, envia a mensagem
        e aguarda uma resposta do servidor. Se ocorrer algum erro, registra a mensagem de erro no log.
        Args:
            ip (str): Endereço IP do destino.
            port (int): Porta do destino.
            msg (str): Mensagem a ser enviada.
        Returns:
            str: Resposta recebida do servidor, ou uma string vazia em caso de erro.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                s.sendall(msg.encode())
                response = s.recv(1024).decode()
                return response
        except Exception as e:
            self.log(f"Erro ao enviar/receber mensagem: {e}")
            return ""