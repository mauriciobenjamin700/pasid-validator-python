from datetime import datetime


def calculate_mrt(messages: list[str]) -> float:
    """
    Calcula o tempo médio de resposta (MRT) a partir de uma lista de mensagens.

    Exemplo de mensagem:

        "1;2;3;4;5;6;7;8;9;10;11.5"
    
    Cada mensagem é uma string com campos separados por ';', onde o último campo é o MRT.
    O MRT é calculado como a média dos valores de MRT extraídos de cada mensagem.

    Args:
        messages (list[str]): Lista de mensagens, onde cada mensagem é uma string com campos separados por ';'.
    Returns:
        float: O tempo médio de resposta (MRT) calculado a partir das mensagens.
    """
    total_mrt = 0
    for message in messages:
        total_mrt += parse_mrt(message)
    return total_mrt / len(messages) if messages else 0

def parse_mrt(message: str) -> float:
    """
    Analisa uma mensagem e extrai o valor do MRT.

    Exemplo de mensagem:

        "1;2;3;4;5;6;7;8;9;10;11.5"

    O MRT é o último campo da mensagem, separado por ponto e vírgula.

    Args:
        message (str): A mensagem a ser analisada, onde o último campo é o MRT.
    Returns:
        float: O valor do MRT extraído da mensagem.
    """
    parts = message.split(";")
    return float(parts[-1])

def extract_mrts(messages: list[str]) -> list[float]:
    """
    Extrai os valores de MRT de uma lista de mensagens.

    Exemplo de mensagem:

        "1;2;3;4;5;6;7;8;9;10;11.5"

    Cada mensagem é uma string com campos separados por ';', onde o último campo é o MRT.

    Args:
        messages (list[str]): Lista de mensagens, onde cada mensagem é uma string com campos separados por ';'.
    Returns:
        list[float]: Lista de valores de MRT extraídos das mensagens.
    """
    return [parse_mrt(message) for message in messages]

def display_results(mrt_from_experiment: float, standard_deviation: float) -> None:
    """
    Exibe os resultados do MRT e do desvio padrão.
    Args:
        mrt_from_experiment (float): O tempo médio de resposta (MRT) calculado a partir das mensagens.
        standard_deviation (float): O desvio padrão dos valores de MRT.
    Returns:
        None
    """
    print(f"MRT From Experiment: {mrt_from_experiment}; SD From Experiment: {standard_deviation}")


def calculate_standard_deviation(mrts: list[float]) -> float:
    """
    Calcula o desvio padrão a partir de uma lista de valores de MRT.

    Args:
        mrts (list[float]): Lista de valores de MRT.
    Returns:
        float: O desvio padrão dos valores de MRT.
    """
    if not mrts:
        return 0.0
    mean = sum(mrts) / len(mrts)
    variance = sum((x - mean) ** 2 for x in mrts) / len(mrts)
    return variance ** 0.5

def calculate_mrt_from_messages(messages: list[str]) -> float:
    """
    Calcula o MRT a partir de uma lista de mensagens.
    Exemplo de mensagem:

        "1;2;3;4;5;6;7;8;9;10;11.5"
    
    Args:
        messages (list[str]): Lista de mensagens, onde cada mensagem é uma string com campos separados por ';'.
    Returns:
        float: O tempo médio de resposta (MRT) calculado a partir das mensagens.
    """
    if not messages:
        return 0.0
    total_mrt = sum(parse_mrt(message) for message in messages)
    return total_mrt / len(messages)

def calculate_mrt_from_experiment(messages: list[str]) -> float:
    """
    Calcula o MRT a partir de uma lista de mensagens.

    Exemplo de mensagem:

        "1;2;3;4;5;6;7;8;9;10;11.5"

    Args:
        messages (list[str]): Lista de mensagens, onde cada mensagem é uma string com campos separados por ';'.
    Returns:
        float: O tempo médio de resposta (MRT) calculado a partir das mensagens.
    """
    if not messages:
        return 0.0
    total_mrt = sum(parse_mrt(message) for message in messages)
    return total_mrt / len(messages)

def get_current_timestamp() -> str:
    """
    Obtém o timestamp atual em segundos desde a época (epoch).
    O timestamp é retornado como uma string representando o tempo atual em segundos.

    Returns:
        str: O timestamp atual em segundos desde a época (epoch).
    """
    now = datetime.now().timestamp()
    return str(now)

def add_timestamp_to_message(message: str) -> str:
    """
    Adiciona um timestamp à mensagem fornecida.
    O timestamp é obtido no formato de segundos desde a época (epoch) e é adicionado ao final da mensagem,
    separado por um ponto e vírgula.

    Args:
        message (str): A mensagem à qual o timestamp será adicionado.

    Returns:
        str: A mensagem original com o timestamp adicionado ao final, no formato "mensagem;timestamp".
    """
    timestamp = get_current_timestamp()
    return f"{message};{timestamp}"