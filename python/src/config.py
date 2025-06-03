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
        'arrival_delay': 0.250, # Tempo de chegada dos clientes em segundos
        #'arrival_delay_variation': 0.5, # Variação do tempo de chegada dos clientes em segundo

        # Configurações do Load Balancer
        'loadbalancers': [
            {
                'name': 'Server1',
                'port': 3000,
                'queue_max_size': 100,
                'qtd_services': 4,
            },
            {
                'name': 'Server2',
                'port': 3100,
                'queue_max_size': 100,
                'qtd_services': 4,
            }
        ],
        # Endereços dos loadbalancers em formato string, se necessário
        'loadbalancer_addresses': "loadbalance1:3000,loadbalance2:3100",
    }