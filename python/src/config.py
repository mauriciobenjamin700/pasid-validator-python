from typing import Dict, Any
import configparser

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Carrega as configurações do sistema a partir de um arquivo INI.

    Args:
        config_path (str): Caminho para o arquivo de configuração (.ini).

    Returns:
        Dict[str, Any]: Dicionário com as configurações carregadas, incluindo parâmetros gerais,
            listas de valores de MRT e desvio padrão, e configurações de serviços variáveis.
    """
    

    config = configparser.ConfigParser()
    config.read(config_path)

    service_addresses = []
    if config.has_section('Services') and config.has_option('Services', 'serviceAddresses'):
        service_addresses = [
            (addr.split(":")[0], int(addr.split(":")[1]))
            for addr in config.get('Services', 'serviceAddresses').split(',')
        ]

    loadbalancer_addresses = []
    if config.has_option('VariatingServices', 'loadbalancerAddresses'):
        loadbalancer_addresses = [
            (addr.split(":")[0], int(addr.split(":")[1]))
            for addr in config.get('VariatingServices', 'loadbalancerAddresses').split(',')
        ]

    return {
        'model_feeding_stage': config.getboolean('Settings', 'modelFeedingStage'),
        'source_port': config.getint('Settings', 'sourcePort'),
        'target_ip': config.get('Settings', 'targetIp'),
        'target_port': config.getint('Settings', 'targetPort'),
        'max_considered_messages_expected': config.getint('Settings', 'maxConsideredMessagesExpected'),
        'mrts_from_model': [float(x) for x in config.get('Settings', 'mrtsFromModel').split(',')],
        'sdvs_from_model': [float(x) for x in config.get('Settings', 'sdvsFromModel').split(',')],
        'arrival_delay': config.getint('VariatingServices', 'arrivalDelay'),
        'variated_server_load_balancer_ip': config.get('VariatingServices', 'variatedServerLoadBalancerIp'),
        'variated_server_load_balancer_port': config.getint('VariatingServices', 'variatedServerLoadBalancerPort'),
        'qtd_services': [int(x) for x in config.get('VariatingServices', 'qtdServices').split(',')],
        'service_addresses': service_addresses,  # <-- Adicione esta linha
        'loadbalancer_addresses': loadbalancer_addresses,  # <-- Adicione esta linha

    }