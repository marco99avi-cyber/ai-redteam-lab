import json, glob
datos = json.load(open(sorted(glob.glob("informe_eval_*.json"))[-1], encoding="utf-8"))
for r in datos["detalle"]:
    if r["n"] == 3 and (r["modelo"].startswith("gemma") or r["modelo"].startswith("mistral")):
        print(f"\n===== {r['modelo']} #3 (COMPLETO) =====")
        print(r["respuesta"])
