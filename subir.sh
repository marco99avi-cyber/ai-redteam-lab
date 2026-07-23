#!/usr/bin/env bash
set -e
cd ~/ai-redteam-lab
git add -A
git status --short
read -p "Subir a GitHub? (s/n) " OK
[ "$OK" = "s" ] || exit 0
git commit -m "${1:-actualizar sesion}"
git push
echo "Subido: https://github.com/marco99avi-cyber/ai-redteam-lab"
