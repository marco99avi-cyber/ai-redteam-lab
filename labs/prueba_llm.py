from llm import preguntar

PROMPT = "Dame en una sola frase una idea para un negocio raro."
MODELO = "mistralai/mistral-small-3.2"

print("=== TEMP 0.0 (dos veces) ===")
for i in range(2):
    r, tok, seg = preguntar(MODELO, PROMPT, 0.0)
    print(f"[{tok} tokens, {seg:.2f}s] {r}")

print("=== TEMP 1.3 (dos veces) ===")
for i in range(2):
    r, tok, seg = preguntar(MODELO, PROMPT, 1.3)
    print(f"[{tok} tokens, {seg:.2f}s] {r}")
