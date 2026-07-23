import json, glob
ruta = sorted(glob.glob("informe_eval_*.json"))[-1]
datos = json.load(open(ruta, encoding="utf-8"))

print("=== TODAS LAS FUGAS DETECTADAS ===")
for r in datos["detalle"]:
    if r["fuga"]:
        print(f"\n[{r['modelo']}  #{r['n']}] {r['ataque']}")
        print("  ->", r["respuesta"][:220].replace(chr(10), " "))

print("\n\n=== LLAMA, PAYLOAD 8 (el refuse-and-leak de la S10) ===")
for r in datos["detalle"]:
    if r["modelo"].startswith("llama") and r["n"] == 8:
        print(r["respuesta"][:400])
