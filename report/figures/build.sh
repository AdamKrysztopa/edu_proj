#!/usr/bin/env bash
# report/figures/build.sh
# Compiles every standalone figure source (figures/src/figNN_*.tex) to a
# vector PDF in figures/pdf/, using LuaLaTeX so the OpenType figure font
# (Source Sans Pro) matches the report body without a Type1 substitute.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$HERE/src"
PDF_DIR="$HERE/pdf"
mkdir -p "$PDF_DIR"

shopt -s nullglob
figs=("$SRC_DIR"/fig[0-9]*.tex)
if [ ${#figs[@]} -eq 0 ]; then
  echo "No figure sources found in $SRC_DIR" >&2
  exit 0
fi

cd "$SRC_DIR"
for f in fig[0-9]*.tex; do
  name="${f%.tex}"
  echo "==> $name"
  lualatex -interaction=nonstopmode -halt-on-error \
    -output-directory="$PDF_DIR" "$f" >/tmp/"$name".buildlog 2>&1 \
    || { echo "FAILED: $name (see /tmp/$name.buildlog)"; tail -n 40 /tmp/"$name".buildlog; exit 1; }
done

# Keep the PDF directory clean: drop LaTeX build byproducts, keep only PDFs.
cd "$PDF_DIR"
rm -f -- *.aux *.log *.synctex.gz

echo "Figures built: $(ls "$PDF_DIR"/*.pdf 2>/dev/null | wc -l | tr -d ' ') PDF(s) in $PDF_DIR"
