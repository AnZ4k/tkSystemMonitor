class Comunicacao():
    def __init__(self, host: str, port: int, tipo: str) -> None:
        self.host = host
        self.port = port
        self.tipo = tipo