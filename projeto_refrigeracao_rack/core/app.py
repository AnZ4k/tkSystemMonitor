import os
from flask import Flask, request
from threading import Lock
import json
from engine import valida_monitores
from time import sleep
import asyncio
from models.auth import Auth
from models.comunicacao import Comunicacao
from models.device import Device
from models.monitores import Monitor

app = Flask(__name__)
lock = Lock()


CDEVICES_CNF_FL = f'core{os.path.sep}devices.json'


async def main() -> None:
    asyncio.create_task(runner_monitor())
    app.run("0.0.0.0")
    
    
@app.route("/registra/<did>", methods=["POST"])
def registro(did):
    data = request.data
    jsn = {}
    
    if not data:
        return json.dumps({"ok": False, "msg": "body nao informado"}), 400

    if not did:
        return json.dumps({"ok": False, "msg": "id do dispositivo nao informado"}), 400
    
    try:
        jsn = json.loads(data)
        try:
            device = Device(
                id=jsn["id"],
                nome=jsn["nome"],
                comunicacao=Comunicacao(
                    host=jsn["comunicacao"]["host"],
                    port=jsn["comunicacao"]["port"],
                    tipo=jsn["comunicacao"]["tipo"]
                ),
                monitores=[Monitor(
                        nome=mon["nome"],
                        vmin=mon["vmin"],
                        vmax=mon["vmax"],
                        vexpected=mon["vexpected"],
                        auth=Auth(
                            required=mon["auth"]["required"],
                            usr=mon["auth"]["usr"],
                            pwd=mon["auth"]["pwd"]
                        )
                    ) for mon in jsn["monitor"]]
            )
            
            _add_device(device=device)
            return  json.dumps({"ok": True, "msg": "cadastrado com sucesso"}), 200
        except Exception as e:
            print("dados invalidos", e)
            return json.dumps({"ok": False, "msg": "erro sintaxe nos dados informados"}), 400
    except:
        print("erro ao parsear json")
        return json.dumps({"ok": False, "msg": "erro sintaxe nos dados informados"}), 400


async def runner_monitor() -> None:
    while True:
        valida_monitores.validar()
        asyncio.sleep(900)


def _config_write(conf: str) -> None:
    with lock:
        file = open(CDEVICES_CNF_FL, 'w')
        file.write(conf)
        file.close()


def _config_read() -> list:
    jsn = []
    
    with open(CDEVICES_CNF_FL, 'r') as fl:
        try:
            jsn = json.loads(fl.read())
            return jsn
        
        except Exception as ex:
            print('Excessao lançada ao abrir configuracao de devices: ', ex)
    
    return []


def _add_device(device: Device) -> bool:
    cnf = _config_read()
    cnf.append(
        {
            "id": device.id,
            "nome": device.nome,
            "comunicacao": {
                "host": device.comunicacao.host,
                "port": device.comunicacao.port,
                "tipo": device.comunicacao.tipo
            },
            "monitor": [{
                "nome": mon.nome,
                "vmin": mon.vmin,
                "vmax": mon.vmax,
                "vexpected": mon.vexpected,
                "auth": {
                    "usr": mon.auth.usr,
                    "pwd": mon.auth.pwd
                }
                } for mon in device.monitores]
        }
    )
    _config_write(json.dumps(cnf, indent=2))


if __name__ == "__main__":
    asyncio.run(main())