def calculate_mrt(messages):
    total_mrt = 0
    for message in messages:
        total_mrt += parse_mrt(message)
    return total_mrt / len(messages) if messages else 0

def parse_mrt(message):
    parts = message.split(";")
    return float(parts[-1])

def extract_mrts(messages):
    return [parse_mrt(message) for message in messages]

def display_results(mrt_from_experiment, standard_deviation):
    print(f"MRT From Experiment: {mrt_from_experiment}; SD From Experiment: {standard_deviation}")