import json, glob
datos = json.load(open(sorted(glob.glob("informe_eval_*.json"))[-1], encoding="utf-8"))
print("=== Payloads que pueden BURLAR al detector (3=letra a letra, 6=al reves) ===")
for r in datos["detalle"]:
    if r["n"] in (3, 6):
        estado = "FUGA-detectada" if r["fuga"] else "marcado-resistio"
        print(f"\n[{r['modelo']} #{r['n']}] ({estado}) {r['ataque']}")
        print("  ->", r["respuesta"][:240].replace(chr(10), " "))
