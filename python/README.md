# PASID Validator Python

Este projeto implementa em Python um sistema distribuído para validação experimental de modelos de desempenho, inspirado em uma arquitetura Java. O sistema é composto por três componentes principais: **Source**, **LoadBalancer** e **Service**, que se comunicam via sockets TCP para simular o envio, balanceamento e processamento de requisições.

## Estrutura do Projeto

```bash
python/
├── docker-compose.yaml        # Orquestração dos containers Docker
├── Dockerfile                 # Dockerfile para build da imagem
├── log.txt                    # Log de execução
├── main.py                    # Script principal para iniciar componentes
├── Makefile                   # Comandos utilitários
├── pyproject.toml             # Configuração de dependências (opcional)
├── requirements.txt           # Dependências Python
├── src/
│   ├── abstract_proxy.py      # Classe base para proxies
│   ├── base.py                # Base de componentes
│   ├── config.py              # Carregamento de configurações (.ini)
│   ├── ia.py                  # (Opcional) Lógica de IA
│   ├── load_balance.py        # Balanceador de carga (round-robin)
│   ├── service.py             # Serviço que processa requisições
│   ├── source.py              # Gerador de requisições
│   ├── utils.py               # Funções utilitárias (MRT, etc)
│   └── configs/
│       ├── source.ini
│       ├── loadbalancer1.ini
│       └── service1.ini
```

## Pré-requisitos

- Python 3.8+
- Docker e Docker Compose (recomendado para execução simplificada)

### Instalação manual (sem Docker)

Instale as dependências:

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

## Execução com Docker

A forma mais simples de rodar o sistema é via Docker Compose. Isso garante que todos os componentes sejam executados em containers isolados, facilitando a configuração e execução.

1. Certifique-se de ter o Docker e o Docker Compose instalados.
2. No diretório `python/`, execute:

```bash
docker compose up --build
```

Os logs dos componentes aparecerão no terminal. Para parar, use `Ctrl+C` e depois:

```bash
docker compose down
```

## Execução manual (sem Docker)

Você pode rodar cada componente separadamente, em diferentes terminais:

```bash
python src/source.py
python src/load_balance.py
python src/service.py
```

Ajuste as configurações de IP/porta conforme necessário nos arquivos `.ini`.

## Resultados

As mensagens entre os componentes geram um resultado onde cada componente adiciona seu timestamp ao final:

```bash
ciclo;id;T_envio;T_chegada_LB;T_saida_LB;T_chegada_SRV;T_saida_SRV
```

O arquivo `log.txt` guarda os resultados do experimento

## Fluxo do Sistema

- O **Source** envia requisições para o **LoadBalancer**.
- O **LoadBalancer** distribui as requisições entre os **Services** disponíveis (round-robin).
- Cada **Service** processa a requisição, simula um tempo de serviço e responde.
- O **Source** coleta as respostas e calcula métricas como MRT (Mean Response Time).
