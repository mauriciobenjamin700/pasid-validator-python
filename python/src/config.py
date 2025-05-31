from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """
    Carrega as configurações do sistema diretamente do código.

    Returns:
        Dict[str, Any]: Dicionário com as configurações carregadas.
    """
    return {
        # Configurações do Source
        'model_feeding_stage': False,
        'source_port': 1000,
        'target_ip': 'localhost',
        'target_port': 2000,
        'max_considered_messages_expected': 10,
        'mrts_from_model': [405597.23, 203892.96],
        'sdvs_from_model': [1245.97, 613.95],
        'qtd_services': [1, 2, 4],
        'arrival_delay': 1000,

        # Configurações dos LoadBalancers
        'loadbalancers': [
            {
                'name': 'Server1',
                'port': 2000,
                'queue_max_size': 100,
                'qtd_services': 4,
            },
            {
                'name': 'Server2',
                'port': 2100,
                'queue_max_size': 100,
                'qtd_services': 4,
            }
        ],
        # Endereços dos loadbalancers em formato string, se necessário
        'loadbalancer_addresses': "loadbalance1:2000,loadbalance2:2100",
    }