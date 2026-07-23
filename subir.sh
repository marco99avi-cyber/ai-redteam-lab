#!/usr/bin/env bash
set -e
cd ~/ai-redteam-lab
cp "/mnt/c/Users/marco/Documents/Cowork OS/Projects/Ciberseguridad"/*.py labs/ 2>/dev/null || true
git add -A
git status --short
read -p "Subir a GitHub? (s/n) " OK
[ "$OK" = "s" ] || exit 0
git commit -m "${1:-actualizar sesion}"
git push
echo "Subido: https://github.com/marco99avi-cyber/ai-redteam-lab"
