## A Makefile to organize our work
SHELL=/bin/sh
DATA_DIR=data

PAPERMILL=poetry run papermill
RSCRIPT=Rscript

NOTEBOOK_SRC_DIR=src/notebooks
NOTEBOOK_OUTPUT_DIR=output/notebooks

R_SRC_DIR=src/R
R_OUTPUT_DIR=output/R

.PHONY: all

# An example of how to set up your Makefile to run an Rmd file from front to back
$(R_OUTPUT_DIR)/011_typical_rmd_file.pdf: $(R_SRC_DIR)/011_typical_rmd_file.Rmd
	$(RSCRIPT) -e "library(rmarkdown); render('$(R_SRC_DIR)/011_typical_rmd_file.Rmd')" && mkdir -p $(R_OUTPUT_DIR) && mv $(R_SRC_DIR)/011_typical_rmd_file.pdf $(R_OUTPUT_DIR)/011_typical_rmd_file.pdf

# An example of how to set up your Makefile to run a notebook from front to back
$(NOTEBOOK_OUTPUT_DIR)/010_typical_notebook_file.ipynb: $(NOTEBOOK_SRC_DIR)/010_typical_notebook_file.ipynb
	mkdir -p $(NOTEBOOK_OUTPUT_DIR) && $(PAPERMILL) $(NOTEBOOK_SRC_DIR)/010_typical_notebook_file.ipynb $(NOTEBOOK_OUTPUT_DIR)/010_typical_notebook_file.ipynb

all: $(R_OUTPUT_DIR)/011_typical_rmd_file.pdf $(NOTEBOOK_OUTPUT_DIR)/010_typical_notebook_file.ipynb

clean:
	rm -f src/R/*.aux src/R/*.fdb_latexmk src/R/*.pdf src/R/*.synctex.gz src/R/*.toc src/R/*.tex src/R/*.md
