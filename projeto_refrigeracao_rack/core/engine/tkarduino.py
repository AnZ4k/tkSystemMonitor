import serial
from .cfg import Configuracao
from time import sleep
"""
modulo responsavel por fazer o controle do modulo rele que ativa o sistema de ventilacao
"""

class Arduino:
    def __init__(self) -> None:
        cfg = Configuracao.read()
        
        self.porta_serial = cfg["porta"]
        self.velocidade_porta = cfg["velocidade"]
        
    
    def ativar(self) -> None:
        self.msg("ativar")
    
    
    def desativar(self) -> None:
        self.msg("desativar")
    
    
    def ativar_prioridade(self) -> None:
        self.msg("ativar_especial")
    
    
    def desativar_prioridade(self) -> None:
        self.msg("desativar_especial")
    
    
    def msg(self, msg: str) -> str:
        
        ser = serial.Serial(self.porta_serial, self.velocidade_porta)
        sleep(5)
        ser.write(f'{msg}\n'.encode())
        sleep(1)
        resp = ser.readline()
        sleep(1)
        ser.close()
        return resp

if __name__ == "__main__":
    ard = Arduino()
    ard.ativar_prioridade()
    sleep(1)
    ard.desativar_prioridade()