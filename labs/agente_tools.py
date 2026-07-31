import requests, json, os

URL    = "http://172.21.0.1:1234/v1/chat/completions"
MODELO = "mistralai/mistral-small-3.2"     # este hace tool calling bien
RAIZ   = os.path.realpath("jaula")          # la caja de S12
SCOPING = True

# ---- las dos herramientas (las MANOS del agente) ----
def leer_archivo(ruta):
    destino = os.path.realpath(os.path.join(RAIZ, ruta))
    if SCOPING and not (destino == RAIZ or destino.startswith(RAIZ + os.sep)):
        return f"[BLOQUEADO por scoping] fuera de la jaula: {ruta}"
    if not os.path.isfile(destino):
        return f"[ERROR] no existe: {ruta}"
    with open(destino, encoding="utf-8", errors="ignore") as f:
        return f.read()

def buscar_web(url):
    try:
        return requests.get(url, timeout=5).text
    except Exception as e:
        return f"[ERROR web] {e}"

DISPATCH = {"leer_archivo": leer_archivo, "buscar_web": buscar_web}

# ---- lo que VE el modelo para decidir (la firma) ----
TOOLS = [
  {"type":"function","function":{
     "name":"leer_archivo",
     "description":"Lee y devuelve el contenido de un archivo del disco local. Usar cuando el usuario pide ver un fichero.",
     "parameters":{"type":"object","properties":{"ruta":{"type":"string"}},"required":["ruta"]}}},
  {"type":"function","function":{
     "name":"buscar_web",
     "description":"Descarga y devuelve el texto de una URL. Usar cuando hace falta informacion de una pagina web.",
     "parameters":{"type":"object","properties":{"url":{"type":"string"}},"required":["url"]}}},
]

def llamar_modelo(messages):
    payload = {"model": MODELO, "messages": messages, "tools": TOOLS, "temperature": 0.0}
    return requests.post(URL, json=payload, timeout=120).json()["choices"][0]["message"]

def agente(pregunta, max_pasos=5):
    messages = [
      {"role":"system","content":"Eres un agente con dos herramientas: leer_archivo y buscar_web. Si el usuario menciona un archivo, llama SIEMPRE a leer_archivo con ese nombre tal cual; NO pidas rutas ni datos al usuario si una herramienta puede conseguirlos."},
      {"role":"user","content":pregunta},
    ]
    for _ in range(max_pasos):
        msg = llamar_modelo(messages)
        tool_calls = msg.get("tool_calls")
        if not tool_calls:
            return msg.get("content","")
        messages.append(msg)
        for tc in tool_calls:
            nombre = tc["function"]["name"]
            args   = json.loads(tc["function"]["arguments"])
            print(f"  -> el modelo PIDE {nombre}({args})")
            resultado = DISPATCH[nombre](**args)
            messages.append({"role":"tool","tool_call_id":tc["id"],"content":str(resultado)})
    return "[sin respuesta final: tope de pasos]"

if __name__ == "__main__":
    print(agente("Resume esta web para mi: http://localhost:8000/pagina.txt"))
