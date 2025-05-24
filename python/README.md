# PASID Validator Python

Este projeto replica em Python um sistema distribuído para validação experimental de modelos de desempenho, inspirado em uma arquitetura Java. O sistema é composto por três componentes principais: **Source**, **LoadBalancer** e **Service**, que se comunicam via sockets TCP para simular o envio, balanceamento e processamento de requisições.

## Estrutura do Projeto

```bash
python/
└── src/
    ├── main.py           # Script principal para iniciar cada componente
    ├── source.py         # Componente gerador de requisições
    ├── load_balancer.py  # Balanceador de carga (round-robin)
    ├── service.py        # Serviço que processa requisições
    ├── config.py         # Carregamento de configurações (.ini)
    ├── utils.py          # Funções utilitárias (MRT, etc)
    └── configs/
        ├── source.ini
        ├── loadbalancer1.ini
        └── service1.ini
```

## Pré-requisitos

- Python 3.8+
- Instale as dependências (se houver) com:

  ```bash
  pip install -r requirements.txt
  ```

## Configuração

Edite os arquivos `.ini` em `src/configs/` para ajustar portas, IPs, tempos de serviço, etc.  
Exemplo de `source.ini`:

```ini
[Settings]
modelFeedingStage = false
sourcePort = 1000
targetIp = localhost
targetPort = 2000
maxConsideredMessagesExpected = 10
mrtsFromModel = 405597.23,203892.96
sdvsFromModel = 1245.97,613.95

[VariatingServices]
arrivalDelay = 100
variatedServerLoadBalancerIp = localhost
variatedServerLoadBalancerPort = 3000
qtdServices = 1,2
```

## Como Executar

Abra **três terminais** (ou mais) e execute cada componente separadamente:

### 1. Inicie os serviços (Service)

Cada serviço escuta em uma porta diferente. Exemplo para dois serviços

```bash
python src/main.py service 3000 100
python src/main.py service 3001 100
```

*(O último argumento é o tempo de serviço em ms)*

### 2. Inicie o LoadBalancer

O LoadBalancer encaminha as requisições para os serviços configurados:

```bash
python src/main.py load_balancer
```

*(Por padrão, encaminha para os serviços nas portas 3000 e 3001)*

### 3. Inicie o Source

O Source lê as configurações e inicia o envio de requisições:

```bash
python src/main.py source
```

## Fluxo do Sistema

- O **Source** envia requisições para o **LoadBalancer**.
- O **LoadBalancer** distribui as requisições entre os **Services** disponíveis (round-robin).
- Cada **Service** processa a requisição, simula um tempo de serviço e responde.
- O **Source** coleta as respostas e calcula métricas como MRT (Mean Response Time).
