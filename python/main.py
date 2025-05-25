import sys


from src.config import load_config
from src.load_balance import LoadBalancer
from src.source import Source
from src.service import Service

def start_source():
    """
    Inicia o serviço de origem que lê dados de um arquivo de configuração
    e envia mensagens para o balanceador de carga.
    O serviço de origem é responsável por ler as mensagens de um arquivo
    e enviá-las para o balanceador de carga, que por sua vez as distribui
    entre os serviços disponíveis.
    Args:
        None

    Returns:
        None
    """

    config = load_config("src/configs/source.ini")
    source = Source(config)
    source.run()

def start_load_balancer(
    listen_port: int = 2000,
    service_addresses: list[tuple[str, int]] = [
        ("localhost", 3000), 
        ("localhost", 3001)
    ]
):
    """
    Inicia o balanceador de carga que escuta em uma porta específica
    e distribui as mensagens recebidas entre os serviços disponíveis.
    O balanceador de carga é responsável por receber as mensagens do serviço de origem
    e encaminhá-las para os serviços disponíveis, garantindo que as mensagens sejam
    processadas de forma eficiente e balanceada entre os serviços.
    Args:
        None
    Returns:
        None
    """

    lb = LoadBalancer(listen_port=listen_port, service_addresses=service_addresses)
    lb.start()

def start_service(port, service_time_ms):
    
    service = Service(listen_port=port, service_time_ms=service_time_ms)
    service.start()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py [source|load_balancer|service] [args...]")
        sys.exit(1)

    role = sys.argv[1]

    if role == "source":
        start_source()
    elif role == "load_balance":
        listen_port = int(sys.argv[2])
        services = []
        if len(sys.argv) > 3:
        # Exemplo: "service1:3000,service2:3001"
            for s in sys.argv[3].split(","):
                host, port = s.split(":")
                services.append((host, int(port)))
        start_load_balancer(
            listen_port=listen_port,
            service_addresses=services if services else [("localhost", 3000), ("localhost", 3001)]
            )
    elif role == "service":
        if len(sys.argv) < 4:
            print("Uso para service: python main.py service <porta> <service_time_ms>")
            sys.exit(1)
        port = int(sys.argv[2])
        service_time_ms = float(sys.argv[3])
        start_service(port, service_time_ms)
    else:
        print("Opção desconhecida:", role)