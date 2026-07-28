import requests
import numpy as np
from llm import preguntar

URL = "http://172.21.0.1:1234/v1/embeddings"
MODELO = "text-embedding-nomic-embed-text-v1.5"
MODELO_CHAT = "llama-3.2-3b-instruct"

# --- aqui van tus dos funciones: embed() y similitud() ---
def embed(texto):
    r = requests.post(URL, json={"model": MODELO, "input": texto})
    return np.array(r.json()["data"][0]["embedding"])
def similitud(a, b):
	numerador = np.dot(a, b)
	denominador = np.linalg.norm(a) * np.linalg.norm(b)
	return numerador / denominador
CORPUS = [
    "Las devoluciones se aceptan hasta 30 dias despues de la compra con el ticket.",
    "El horario de la tienda es de lunes a viernes de 9 a 20 horas.",
    "Para reembolsos, el dinero tarda entre 3 y 5 dias habiles en volver a tu cuenta.",
    "La garantia de los productos electronicos es de 2 anios desde la fecha de compra.",
    "Hacemos envios a toda la peninsula en 24-48 horas por 4.99 euros.",
    "El cafe de la maquina del pasillo cuesta 60 centimos.",
]

# indexamos una sola vez: cada doc con su vector
INDICE = [(doc, embed(doc)) for doc in CORPUS]

def buscar(pregunta, k=3):
    v = embed(pregunta)
    rankeados = sorted(INDICE, key=lambda par: similitud(v, par[1]), reverse=True)
    return rankeados[:k]

def responder(pregunta):
    contexto = "\n".join(doc for doc, vec in buscar(pregunta))
    prompt = (
        "Responde SOLO con la informacion del contexto. "
        "Si no esta en el contexto, di que no lo sabes.\n\n"
        "CONTEXTO:\n" + contexto + "\n\nPREGUNTA: " + pregunta
    )
    return preguntar(MODELO_CHAT, prompt, 0.0)

if __name__ == "__main__":
    for p in ["cuanto tiempo tengo para devolver algo?",
              "quien gano el mundial de 2010?"]:
        print("P:", p)
        print("R:", responder(p))
        print("---")
