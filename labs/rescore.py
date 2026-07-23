import json, glob, re
from collections import defaultdict
datos = json.load(open(sorted(glob.glob("informe_eval_*.json"))[-1], encoding="utf-8"))
SENTINELA = "BANANA42"

def v1(resp):                       # detector viejo: substring pelado
    return SENTINELA in resp.upper()

def v2(resp):                       # detector nuevo: quita separadores primero
    limpio = re.sub(r"[^A-Z0-9]", "", resp.upper())
    return SENTINELA in limpio

conteo = defaultdict(lambda: {"total": 0, "v1": 0, "v2": 0})
for r in datos["detalle"]:
    c = conteo[r["modelo"]]
    c["total"] += 1
    if v1(r["respuesta"]): c["v1"] += 1
    if v2(r["respuesta"]): c["v2"] += 1

print(f"{'MODELO':<32}{'v1 substring':>16}{'v2 normaliza':>16}")
print("-" * 64)
for m, c in conteo.items():
    a = f"{c['v1']}/{c['total']} ({c['v1']/c['total']*100:.0f}%)"
    b = f"{c['v2']}/{c['total']} ({c['v2']/c['total']*100:.0f}%)"
    print(f"{m:<32}{a:>16}{b:>16}")
