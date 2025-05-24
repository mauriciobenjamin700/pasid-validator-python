import socket
import threading
import time
from typing import List, Dict, Any

class Source:
    """
    Classe responsável por gerar e enviar mensagens para o sistema distribuído.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self.model_feeding_stage: bool = config.get("model_feeding_stage", False)
        self.arrival_delay: int = config.get("arrival_delay", 0)
        self.max_considered_messages_expected: int = config.get("max_considered_messages_expected", 10)
        self.source_current_index_message: int = 0
        self.considered_messages: List[str] = []
        self.qtd_services: List[int] = config.get("qtd_services", [])
        self.cycles_completed: List[bool] = [False] * len(self.qtd_services)
        self.dropp_count: int = 0
        self.log_file: str = "log.txt"
        self.target_ip: str = config.get("target_ip", "localhost")
        self.target_port: int = config.get("target_port", 2000)
        self.init_log_file()

    def init_log_file(self) -> None:
        with open(self.log_file, 'w') as f:
            f.write("")

    def log(self, message: str) -> None:
        print(message)
        with open(self.log_file, 'a') as f:
            f.write(message + "\n")

    def run(self) -> None:
        self.log("Starting source")
        if self.model_feeding_stage:
            self.send_message_feeding_stage()
        else:
            self.send_messages_validation_stage()

    def send_message_feeding_stage(self) -> None:
        self.log("Model Feeding Stage Started")
        for _ in range(10):
            msg = f"1;{self.source_current_index_message};{self.get_current_time()}"
            self.send(msg)
            self.source_current_index_message += 1
            time.sleep(self.arrival_delay / 1000.0)

    def send_messages_validation_stage(self) -> None:
        for cycle, qts in enumerate(self.qtd_services):
            self.source_current_index_message = 1
            self.considered_messages.clear()
            config_message = f"config;{qts}"
            self.send_message_to_configure_server(config_message)

            threads = []
            for _ in range(self.max_considered_messages_expected):
                msg = f"{cycle};{self.source_current_index_message};{self.get_current_time()}"
                t = threading.Thread(target=self.send_and_receive, args=(msg, cycle))
                t.start()
                threads.append(t)
                self.source_current_index_message += 1
                time.sleep(self.arrival_delay / 1000.0)

            for t in threads:
                t.join()

            self.cycles_completed[cycle] = True
            self.log(f"Ciclo {cycle} finalizado.")

    def send_message_to_configure_server(self, config_message: str) -> None:
        self.send(config_message)

    def send(self, msg: str) -> None:
        """Envia uma mensagem para o destino."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.target_ip, self.target_port))
                s.sendall(msg.encode())
        except Exception as e:
            self.log(f"Erro ao enviar mensagem: {e}")

    def send_and_receive(self, msg: str, cycle: int) -> None:
        """Envia uma mensagem e aguarda a resposta."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.target_ip, self.target_port))
                s.sendall(msg.encode())
                response = s.recv(1024).decode()
                self.considered_messages.append(response)
                self.log(f"Recebido no ciclo {cycle}: {response}")
        except Exception as e:
            self.log(f"Erro ao enviar/receber mensagem: {e}")

    def get_current_time(self) -> int:
        return int(time.time() * 1000)

    def close_log(self) -> None:
        pass