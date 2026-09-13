#!/bin/bash
# Install LiCus dependencies
# Run with: bash dependencies_install.sh

set -e

echo "== Updating package lists =="
sudo pacman -Syu

echo "== Installing system package: git, wine, gamemode, unzip, python-pip =="
sudo pacman -S git wine gamemode unzip python-pip

echo "== Installing needed Python libraries: rich, pynput =="
pip install --break-system-packages rich pynput

echo ""
echo "== Verifying installs =="
for cmd in git wine gamemoderun unzip; do
    if command -v "$cmd" >/dev/null 2>&1; then
        echo "[OK] $cmd found"
    else
        echo "[FAIL] $cmd not found"
    fi
done

python -c "import rich" 2>/dev/null && echo "[OK] rich can be import" || echo "[FAILED] rich CANNOT be import"
python -c "import pynput" 2>/dev/null && echo "[OK] pynput can be import" || echo "[FAILED] pynput CANNOT be import"

echo ""
echo "Done. If anything shows [FAILED], re-run the install command manually."