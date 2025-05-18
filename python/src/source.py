class Source:
    def __init__(self, config):
        self.json_path = config.get("json_path")
        self.model_feeding_stage = config.get("model_feeding_stage", False)
        self.arrival_delay = config.get("arrival_delay", 0)
        self.max_considered_messages_expected = config.get("max_considered_messages_expected", 10)
        self.source_current_index_message = 0
        self.considered_messages = []
        self.qtd_services = config.get("qtd_services", [])
        self.cycles_completed = [False] * len(self.qtd_services)
        self.dropp_count = 0
        self.log_file = "log.txt"
        self.init_log_file()

    def init_log_file(self):
        with open(self.log_file, 'w') as f:
            f.write("")

    def log(self, message):
        print(message)
        with open(self.log_file, 'a') as f:
            f.write(message + "\n")

    def run(self):
        self.log("Starting source")
        if self.model_feeding_stage:
            self.send_message_feeding_stage()
        else:
            self.send_messages_validation_stage()

    def send_message_feeding_stage(self):
        self.log("Model Feeding Stage Started")
        for _ in range(10):
            msg = f"1;{self.source_current_index_message};{self.get_current_time()};\n"
            self.send(msg)
            self.source_current_index_message += 1

    def send_messages_validation_stage(self):
        for cycle, qts in enumerate(self.qtd_services):
            self.source_current_index_message = 1
            self.considered_messages.clear()
            config_message = f"config;{qts};\n"
            self.send_message_to_configure_server(config_message)

            for _ in range(self.max_considered_messages_expected):
                msg = f"{cycle};{self.source_current_index_message};{self.get_current_time()};\n"
                self.send(msg)
                self.source_current_index_message += 1

            while not self.cycles_completed[cycle]:
                pass  # Wait for cycle to complete

    def send_message_to_configure_server(self, config_message):
        # Implementation for sending configuration message to server
        pass

    def send(self, msg):
        # Implementation for sending messages to the destination
        pass

    def get_current_time(self):
        import time
        return int(time.time() * 1000)  # Current time in milliseconds

    def receiving_messages(self, new_socket_connection):
        # Implementation for receiving messages
        pass

    def execute_first_stage_of_model_feeding(self, received_message):
        # Implementation for processing received messages in feeding stage
        pass

    def execute_second_stage_of_validation(self, received_message):
        # Implementation for processing received messages in validation stage
        pass

    def close_log(self):
        # Implementation for closing log file if necessary
        pass