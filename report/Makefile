# report/Makefile
# `make`          -> figures, then all three documents
# `make figures`  -> compile figures/src/*.tex to figures/pdf/*.pdf
# `make extended` -> main.tex -> extended_technical_report.pdf (the complete technical record)
# `make main`     -> short.tex -> main_research_report.pdf (the argument, <= 40 pages of main content)
# `make summary`  -> summary.tex -> executive_summary.pdf (2 pages; needs build/main.aux, so runs after extended)
# `make clean`    -> remove build/ (keeps the PDFs)

.PHONY: all figures extended main summary clean

all: extended main summary

figures:
	bash figures/build.sh

extended: figures
	latexmk -r latexmkrc main.tex
	cp build/main.pdf extended_technical_report.pdf

main: figures
	latexmk -r latexmkrc short.tex
	cp build/short.pdf main_research_report.pdf

summary: extended
	latexmk -r latexmkrc summary.tex
	cp build/summary.pdf executive_summary.pdf

clean:
	rm -rf build
