#!/usr/bin/env bash
# Linux: modo sem saída para a rede. Baixe os pesos com ia.py preparar primeiro.
set -euo pipefail
AQUI=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
command -v bwrap >/dev/null || { echo "Instale bubblewrap (Ubuntu: sudo apt install bubblewrap iproute2)." >&2; exit 2; }
command -v ip >/dev/null || { echo "Instale iproute2 (Ubuntu: sudo apt install iproute2)." >&2; exit 2; }
[ "${1:-conversar}" != preparar ] || { echo "Preparar precisa de internet: use python3 ia.py preparar fora deste modo." >&2; exit 2; }
[ "$#" -gt 0 ] || set -- conversar
# O argumento do Python é posicional: nenhum texto do usuário vira código shell.
exec bwrap --unshare-user --unshare-net --die-with-parent --dev-bind / / --proc /proc   --cap-add CAP_NET_ADMIN /bin/sh -c 'ip link set lo up && exec python3 "$@"' sh "$AQUI/ia.py" "$@"
