class AbstractProxy:
    """
    Classe base para proxies que implementam funcionalidades de log e controle de tempo.
    Esta classe fornece métodos para inicializar um arquivo de log, registrar mensagens e obter o tempo atual em milissegundos.
    O arquivo de log é utilizado para registrar as mensagens enviadas e recebidas.

    Args:
        log_file (str): O caminho do arquivo de log. Padrão é "log.txt".
    
    Attributes:
        log_file (str): O caminho do arquivo de log onde as mensagens serão registradas.
        
    Methods:
        init_log_file(): Inicializa o arquivo de log, limpando seu conteúdo.
        log(message: str): Registra uma mensagem no log e no console.
    """
    def __init__(self, log_file="log.txt"):
        self.log_file = log_file
        self.init_log_file()

    def init_log_file(self):
        with open(self.log_file, 'w') as f:
            f.write("")

    def log(self, message: str):
        print(message)
        with open(self.log_file, 'a') as f:
            f.write(message + "\n")
