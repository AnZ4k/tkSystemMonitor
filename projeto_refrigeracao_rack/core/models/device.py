from .comunicacao import Comunicacao

class Device():
    def __init__(self, id: str, nome: str, comunicacao: Comunicacao, monitores: list) -> None:
        self.id = id
        self.nome = nome
        self.comunicacao = comunicacao
        self.monitores = monitores