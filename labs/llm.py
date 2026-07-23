import requests
import time

URL = "http://172.21.0.1:1234/v1/chat/completions"

def preguntar(modelo, prompt, temp, system=None):
    mensajes = []
    if system is not None:
        mensajes.append({"role": "system", "content": system})
    mensajes.append({"role": "user", "content": prompt})

    payload = {
        "model": modelo,
        "messages": mensajes,
        "temperature": temp
    }
    t0 = time.time()
    respuesta_http = requests.post(URL, json=payload)
    tiempo = time.time() - t0
    datos = respuesta_http.json()
    texto  = datos["choices"][0]["message"]["content"]
    tokens = datos["usage"]["total_tokens"]
    return texto, tokens, tiempo
