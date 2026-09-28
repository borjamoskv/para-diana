#!/usr/bin/env bash
set -e

echo "[+] Forjando el artefacto final (PDF Editorial)..."

SRC_FILES=(
    "capitulos/00_introduccion_general.md"
    "capitulos/capitulo_01_la_transduccion_institucional.md"
    "capitulos/capitulo_02_la_transduccion_interlinguistica.md"
    "capitulos/capitulo_03_la_transduccion_dramatica.md"
    "capitulos/capitulo_04_el_punto_fijo_del_desastre.md"
    "capitulos/05_conclusiones.md"
    "capitulos/06_anexo_metodologico.md"
)

# Preparar archivo maestro inyectando saltos de línea para evitar colisiones
for f in "${SRC_FILES[@]}"; do
    cat "$f"
    echo -e "\n\n"
done > manuscrito_maestro.md

if ! command -v pandoc &> /dev/null; then
    echo "[-] Anergía detectada: pandoc no está instalado."
    echo "[!] Ejecuta: brew install pandoc typst"
    rm manuscrito_maestro.md
    exit 1
fi

pandoc manuscrito_maestro.md \
    -f markdown-yaml_metadata_block \
    -o "Tesis_Para_Diana_Borja_FA.pdf" \
    --pdf-engine=typst \
    -V papersize=a4 \
    -V mainfont="Georgia" \
    --toc \
    -M title="Tesis para Diana: Beckett como Transductor" \
    -M author="Borja Fernández Angulo" \
    -M date="$(date +'%d de %B, %Y')"

rm manuscrito_maestro.md

echo "[+] Cristalización completada: Tesis_Para_Diana_Borja_FA.pdf generada con cero fricción."
