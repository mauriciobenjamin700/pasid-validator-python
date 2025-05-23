def calculate_mrt(messages: list[str]) -> float:
    """
    Calculates the Mean Response Time (MRT) from a list of messages.

    example:
        "1234;2024-05-23T15:00:00Z;0.153"
    
    Where:
        - 1234 is the message ID
        - 2024-05-23T15:00:00Z is the timestamp
        - 0.153 is the MRT value

    Args:
        messages (list[str]): list of message strings.

    Returns:
        float: The calculated MRT, or 0 if the list is empty.
    """
    total_mrt = 0
    for message in messages:
        total_mrt += parse_mrt(message)
    return total_mrt / len(messages) if messages else 0

def parse_mrt(message: str) -> float:
    """
    Parses the MRT value from a message string.

    Args:
        message (str): The message string, fields separated by ';'.

    Returns:
        float: The MRT value extracted from the message.
    """
    parts = message.split(";")
    return float(parts[-1])

def extract_mrts(messages: list[str]) -> list[float]:
    """Extracts MRT values from a list of messages.

    Args:
        messages (list[str]): list of message strings.

    Returns:
        list[float]: list of MRT values.
    """
    return [parse_mrt(message) for message in messages]

def display_results(mrt_from_experiment: float, standard_deviation: float) -> None:
    """
    Displays the MRT and standard deviation results.

    Args:
        mrt_from_experiment (float): The experimental MRT value.
        standard_deviation (float): The standard deviation value.
    """
    print(f"MRT From Experiment: {mrt_from_experiment}; SD From Experiment: {standard_deviation}")