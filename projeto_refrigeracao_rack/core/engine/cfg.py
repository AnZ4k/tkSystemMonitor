from threading import Lock
import json
import os

lock = Lock

class Configuracao:
    def read() -> map:
        with open(f"core{os.path.sep}engine{os.path.sep}config.json", 'r') as fl:
            return json.loads(fl.read())
        
        
    def write(cfg: map) -> None:
        with lock:
            with open('./config.json', 'w') as fl:
                fl.write(json.dumps(cfg))
