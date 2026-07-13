#!/bin/sh
# Compila los papers a PDF con la cadena usada en el repo: pandoc → Chrome headless.
#
#   paper/build.sh                      # compila paper1_metodo y paper2_desigualdad
#   paper/build.sh paper2_desigualdad   # compila solo uno
#
# Requisitos: pandoc y Google Chrome (el estilo vive en paper/paper.css; las figuras
# se resuelven por ruta relativa ../figures/, así que el repo debe estar completo).
# El título del PDF es el H1 hasta los dos puntos (igual que los PDFs originales).
set -eu
cd "$(dirname "$0")"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"

[ $# -eq 0 ] && set -- paper1_metodo paper2_desigualdad
for name in "$@"; do
  title=$(sed -n '1s/^# //p' "$name.md" | sed 's/:.*//')
  pandoc "$name.md" -f markdown+smart -t html5 -s \
    --metadata pagetitle="$title" --css=paper.css -o "$name.html"
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$name.pdf" "$name.html" 2>/dev/null
  rm "$name.html"
  echo "✓ $name.pdf"
done
