import sys
from config import load_config

def start_source():
    from source import Source
    config = load_config("src/configs/source.ini")
    source = Source(config)
    source.run()

def start_load_balancer():
    from load_balance import LoadBalancer
    # Exemplo: carrega de um arquivo ou define manualmente
    # Aqui, para exemplo, services nas portas 3000 e 3001
    service_addresses = [("localhost", 3000), ("localhost", 3001)]
    lb = LoadBalancer(listen_port=2000, service_addresses=service_addresses)
    lb.start()

def start_service(port, service_time_ms):
    from service import Service
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
        start_load_balancer()
    elif role == "service":
        if len(sys.argv) < 4:
            print("Uso para service: python main.py service <porta> <service_time_ms>")
            sys.exit(1)
        port = int(sys.argv[2])
        service_time_ms = float(sys.argv[3])
        start_service(port, service_time_ms)
    else:
        print("Opção desconhecida:", role)