from .auth import Auth

class Monitor():
    def __init__(self, nome: str, auth: Auth, vmin: float = 0.0, vmax: float = 0.0, vexpected: list = []) -> None:
        self.nome = nome,
        self.vmin = vmin,
        self.vmax = vmax
        self.vexpected = vexpected
        self.auth = auth