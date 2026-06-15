"""
ataque_llm.py — Mi primer script de ataque a un LLM local.

Qué hace: manda un prompt a mi modelo de LM Studio (corriendo en mi PC)
a través de su API, y me imprime la respuesta del modelo.

Es el esqueleto de toda automatizacion de ataques que hare mas adelante:
en vez de escribir prompts a mano en una web, los mando por codigo.

Autor: Marco — Sesion 2
"""

# 'requests' es la libreria que deja a Python hablar por HTTP (como hace curl).
import requests

# --- CONFIGURACION ---------------------------------------------------------

# La "puerta" donde escucha mi LM Studio. Desde WSL uso la IP de Windows
# (localhost NO funciona desde WSL). Si trabajara en Windows directo, seria
# "http://localhost:1234".
URL = "http://192.168.1.45:1234/v1/chat/completions"

# Que modelo quiero atacar. Tengo varios cargados; empiezo con el pequeño.
MODELO = "llama-3.2-3b-instruct"

# --- EL ATAQUE -------------------------------------------------------------

# Este es el prompt que le mando al modelo. Cambiando ESTA linea pruebo
# distintos ataques. Empiezo con algo inofensivo para verificar que funciona.
prompt = "Preséntate en una frase. ¿Quién eres?"

# La API espera los datos en este formato (estilo OpenAI). 'messages' es la
# conversacion: cada mensaje tiene un 'role' (user = yo) y un 'content' (el texto).
datos = {
    "model": MODELO,
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.7,  # creatividad: 0 = robotico, 1 = mas variado
}

# --- ENVIAR Y LEER ---------------------------------------------------------

print(f"[*] Atacando a {MODELO}...")
print(f"[*] Prompt enviado: {prompt}\n")

# Mando la peticion POST con mis datos en formato JSON.
respuesta = requests.post(URL, json=datos)

# Convierto la respuesta (que viene en JSON) en algo que Python entiende.
resultado = respuesta.json()

# Saco SOLO el texto que dijo el modelo, navegando por la estructura del JSON.
# Es el mismo camino que vi con curl: choices -> [0] -> message -> content.
texto_modelo = resultado["choices"][0]["message"]["content"]

print("[+] El modelo respondio:\n")
print(texto_modelo)
