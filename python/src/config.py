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
        'qtd_services': [int(x) for x in config.get('VariatingServices', 'qtdServices').split(',')]
    }