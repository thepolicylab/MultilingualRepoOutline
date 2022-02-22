## A Makefile to organize our work
SHELL=/bin/sh
DATA_DIR_UNVAX=data/unvax_data/output
DATA_DIR=data
R_SRC_DIR=src/R/300_wrangling
R_ANALYSIS_DIR=src/R/400_analysis
R_OUTPUT_DIR=$(R_ANALYSIS_DIR)/output

.PHONY: all


## We use this for everything but the ZCTA level analysis.
## See the effects_on_vaccinations.Rmd file for more details.
$(DATA_DIR)/dat_indiv.csv: $(R_SRC_DIR)/010_counts_from_vax_list_data_setup.R \
	$(DATA_DIR)/counts_from_vax_list_anytime_after_send.csv \
	$(DATA_DIR)/counts_from_vax_list_within_one_week_after_send.csv
	R --file=$(R_SRC_DIR)/010_counts_from_vax_list_data_setup.R

## effects_on_vaccinations.Rmd creates all of the figures for the paper.
## they are saved one at a time in R_OUTPUT_DIR alone with the report itself.
$(R_OUTPUT_DIR)/effects_on_vaccinations.pdf: $(DATA_DIR)/dat_indiv.csv \
	$(DATA_DIR)/final_data_one_line_per_individual.csv \
	$(DATA_DIR)/combined_demo_data_by_zcta.csv \
	$(R_ANALYSIS_DIR)/000_constants.R \
	$(R_ANALYSIS_DIR)/010_rmd_setup.R \
	$(R_ANALYSIS_DIR)/020_effects_on_vaccinations.Rmd
	Rscript -e "library(rmarkdown); render('src/R/400_analysis/020_effects_on_vaccinations.Rmd')" && mv $(R_ANALYSIS_DIR)/020_effects_on_vaccinations.pdf $(R_OUTPUT_DIR)/effects_on_vaccinations.pdf

$(R_OUTPUT_DIR)/effects_on_vaccinations.docx: $(DATA_DIR)/dat_indiv.csv \
	$(DATA_DIR)/final_data_one_line_per_individual.csv \
	$(DATA_DIR)/combined_demo_data_by_zcta.csv \
	$(R_ANALYSIS_DIR)/000_constants.R \
	$(R_ANALYSIS_DIR)/010_rmd_setup.R \
	$(R_ANALYSIS_DIR)/020_effects_on_vaccinations.Rmd
	Rscript -e "library(rmarkdown); render('src/R/400_analysis/020_effects_on_vaccinations.Rmd',output_format=word_document())" && mv $(R_ANALYSIS_DIR)/020_effects_on_vaccinations.docx $(R_OUTPUT_DIR)/effects_on_vaccinations.docx

## Figures created within 020_effects_on_vaccinations.Rmd
$(R_OUTPUT_DIR)/rq2_rq7_plot.pdf: $(R_OUTPUT_DIR)/effects_on_vaccinations.pdf
$(R_OUTPUT_DIR)/day_by_day_plot.pdf: $(R_OUTPUT_DIR)/effects_on_vaccinations.pdf
$(R_OUTPUT_DIR)/combined_plot.pdf: $(R_OUTPUT_DIR)/effects_on_vaccinations.pdf

all: $(DATA_DIR)/dat_indiv.csv $(R_OUTPUT_DIR)/effects_on_vaccinations.pdf $(R_OUTPUT_DIR)/effects_on_vaccinations.docx
