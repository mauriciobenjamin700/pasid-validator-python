import socket
import threading
import time
from typing import List, Dict, Any

from src.abstract_proxy import AbstractProxy
from src.utils import get_current_timestamp

class Source(AbstractProxy):
    """
    Classe responsável por gerar e enviar mensagens para o sistema distribuído.

    Esta classe pode operar em dois estágios:
    1. **Model Feeding Stage**: Envia mensagens de alimentação do modelo.
    2. **Validation Stage**: Envia mensagens de validação, configurando o número de serviços e aguardando respostas.
    Args:
        config (Dict[str, Any]): Configurações para a classe Source, incluindo:
            - model_feeding_stage (bool): Indica se está no estágio de alimentação do modelo.
            - arrival_delay (int): Atraso em milissegundos entre o envio de mensagens.
            - max_considered_messages_expected (int): Número máximo de mensagens consideradas por ciclo.
            - qtd_services (List[int]): Lista com a quantidade de serviços disponíveis.
            - target_ip (str): IP do destino para envio das mensagens.
            - target_port (int): Porta do destino para envio das mensagens.
        Esta classe é responsável por enviar mensagens para um servidor de destino,
        gerenciar ciclos de envio e receber respostas, registrando logs das operações.
        Além disso, ela mantém o controle do estado dos ciclos e mensagens consideradas.

    Attributes:
        model_feeding_stage (bool): Indica se está no estágio de alimentação do modelo.
        arrival_delay (int): Atraso em milissegundos entre o envio de mensagens.
        max_considered_messages_expected (int): Número máximo de mensagens consideradas por ciclo.
        source_current_index_message (int): Índice atual da mensagem a ser enviada.
        considered_messages (List[str]): Lista de mensagens consideradas.
        qtd_services (List[int]): Lista com a quantidade de serviços disponíveis.
        cycles_completed (List[bool]): Lista indicando se os ciclos foram completados.
        dropp_count (int): Contador de mensagens descartadas.
        target_ip (str): IP do destino para envio das mensagens.
        target_port (int): Porta do destino para envio das mensagens.

    Methods:
        log(message: str): Registra uma mensagem no log e no console.
        run(): Inicia o processo de envio de mensagens.
        send_message_feeding_stage(): Envia mensagens no estágio de alimentação do modelo.
        send_messages_validation_stage(): Envia mensagens no estágio de validação.
        send_message_to_configure_server(config_message: str): Envia uma mensagem de configuração ao servidor.
        send(msg: str): Envia uma mensagem para o destino especificado.
        send_and_receive(msg: str, cycle: int): Envia uma mensagem e aguarda a resposta do servidor.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__()
        self.model_feeding_stage: bool = config.get("model_feeding_stage", False)
        self.arrival_delay: int = config.get("arrival_delay", 0)
        self.max_considered_messages_expected: int = config.get("max_considered_messages_expected", 10)
        self.source_current_index_message: int = 0
        self.considered_messages: List[str] = []
        self.qtd_services: List[int] = config.get("qtd_services", [])
        self.cycles_completed: List[bool] = [False] * len(self.qtd_services)
        self.dropp_count: int = 0
        self.loadbalancer_addresses = config.get("loadbalancer_addresses", "")
        if isinstance(self.loadbalancer_addresses, str):
            self.loadbalancer_addresses = [
                (address.split(":")[0], int(address.split(":")[1]))
                for address in self.loadbalancer_addresses.split(",")
            ]

    def run(self) -> None:
        """
        Inicia o processo de envio de mensagens.
        Dependendo do estágio (alimentação do modelo ou validação),
        chama o método apropriado para enviar mensagens.
        O método `send_message_feeding_stage` é chamado se o estágio for de alimentação do modelo,
        enquanto `send_messages_validation_stage` é chamado para o estágio de validação.
        O método `send_messages_validation_stage` também configura o número de serviços
        e aguarda as respostas dos serviços.

        Args:
            None
        Returns:
            None
        """
        self.sys_log("Starting source")
        if self.model_feeding_stage:
            self.sys_log("Model Feeding Stage Enabled")
            # TODO: FUTURAMENTE DARIA PRA USAR ALGO DE TESTE AQUI
            self.send_message_feeding_stage()
        else:
            self.sys_log("Validation Stage Enabled")
            self.send_messages_validation_stage()

    def send_message_feeding_stage(self) -> None:
        """
        Envia mensagens no estágio de alimentação do modelo.
        Neste estágio, as mensagens são enviadas em um loop,
        com um atraso definido entre cada envio.
        O método `send` é chamado para enviar as mensagens.
        O índice da mensagem é incrementado a cada envio.
        O método `get_current_timestamp` é utilizado para obter o timestamp atual
        e incluir na mensagem enviada.

        Args:
            None
        Returns:
            None
        """
        self.log("Model Feeding Stage Started")
        for _ in range(10):
            msg = f"1;{self.source_current_index_message};{get_current_timestamp()}"
            self.send(msg)
            self.source_current_index_message += 1
            time.sleep(self.arrival_delay)

    def send_messages_validation_stage(self) -> None:
        """
        Envia mensagens no estágio de validação.
        Neste estágio, as mensagens são enviadas em ciclos,
        com um atraso definido entre cada envio.
        O método `send_message_to_configure_server` é chamado para enviar a configuração do servidor.
        O método `send_and_receive` é chamado para enviar mensagens e aguardar as respostas.
        O índice da mensagem é incrementado a cada envio.
        O método `get_current_timestamp` é utilizado para obter o timestamp atual
        e incluir na mensagem enviada.

        Args:
            None
        Returns:
            None
        """
        self.sys_log(F"Validation Stage Started: TO {self.qtd_services} services")
        for cycle, qts in enumerate(self.qtd_services):
            self.source_current_index_message = 1
            self.considered_messages.clear()

            # Distribui as mensagens entre os load balancers
            num_balancers = len(self.loadbalancer_addresses)
            self.sys_log("Load Balances available: " + str(self.loadbalancer_addresses))
            start_time = time.time()
            #timeout = 10  # segundos
            threads: list[threading.Thread] = []
            self.sys_log(f"Starting cycle {cycle} with {qts} services")
            self.sys_log(f"Max considered messages expected: {self.max_considered_messages_expected}")
            for i in range(self.max_considered_messages_expected):
                # Escolhe o load balancer de forma round-robin
                lb_ip, lb_port = self.loadbalancer_addresses[i % num_balancers]
                self.sys_log(f"Sending message to load balancer {lb_ip}:{lb_port} in cycle {cycle}")
                # TODO: GAMBIARRA DNV, DESGRAAAA
                if lb_port == 3000:
                    service_addresses = [
                        "service1:3001",
                        "service2:3002",
                        "service3:3003",
                        "service4:3004"
                    ]
                elif lb_port == 3100:
                    service_addresses = [
                        "service11:3101",
                        "service12:3102",
                        "service13:3103",
                        "service14:3104"
                    ]
                else:
                    self.sys_log(f"Unsupported load balancer port: {lb_port}")
                    raise ValueError(f"Unsupported load balancer port: {lb_port}")
                config_message = "config;" + ",".join(service_addresses[0:cycle+1])
                self.sys_log(f"Sending config message to {lb_ip}:{lb_port}: {config_message}")

                self.send_message_to_configure_server(config_message, lb_ip, lb_port)

                msg = f"{cycle};{self.source_current_index_message};{get_current_timestamp()}"
                t = threading.Thread(target=self.send_and_receive_to_lb, args=(lb_ip, lb_port, msg, cycle))
                t.start()
                threads.append(t)
                self.source_current_index_message += 1
                time.sleep(self.arrival_delay)

            for t in threads:
                #t.join(timeout=max(0, timeout - (time.time() - start_time)))
                t.join()

            self.cycles_completed[cycle] = True
            self.log(f"Ciclo {cycle} finalizado.")

    def send_message_to_configure_server(self, config_message: str, ip: str, port: int) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                s.sendall(config_message.encode())
        except Exception as e:
            self.log(f"Erro ao enviar mensagem de configuração para {ip}:{port}: {e}")

    def send(self, msg: str) -> None:
        """
        Envia uma mensagem para o destino especificado.
        O método utiliza um socket TCP para enviar a mensagem.
        O IP e a porta do destino são definidos nas configurações da classe.
        O método `get_current_timestamp` é utilizado para obter o timestamp atual
        e incluir na mensagem enviada.

        Args:
            msg (str): Mensagem a ser enviada.
        Returns:
            None
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.target_ip, self.target_port))
                s.sendall(msg.encode())
        except Exception as e:
            self.log(f"Erro ao enviar mensagem: {e}")

    def send_and_receive_to_lb(self, ip: str, port: int, msg: str, cycle: int) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                s.sendall(msg.encode())
                response = s.recv(1024).decode()
                self.considered_messages.append(response)
                self.log(f"Recebido de {ip}:{port} no ciclo {cycle}: {response}")
        except Exception as e:
            self.log(f"Erro ao enviar/receber mensagem para {ip}:{port}: {e}")
