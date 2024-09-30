import requests
import json

def coleta_informacoes(host: str, port: int) -> map:
    resposta = requests.get(f"http://{host}:{port}/get-info")
    jsn = {}
    
    if resposta.status_code == 200:
        jsn_resp = json.loads(resposta.text)
        
        if jsn_resp["ok"]:
            jsn = json.loads(json.loads(resposta.text)["msg"])
        
    return jsn    