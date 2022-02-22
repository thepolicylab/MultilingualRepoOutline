# Basic Code Repository

## Overview

This repository contains the basic outline of an analysis repository that plans for
our typical need to support many different languanges among all of our project partners.

When you start a new repository based on this one, you should replace this overview
with an actual project overview and delete whatever requirements descriptions you
do not need from the below.

## Requirements

### Software

To run the code in this repository, you will need Python 3.8+ and R 4.0.2+ pre-installed.
We also require SPSS version 16.

In Python, we use [`poetry`](https://python-poetry.org/) to manage our dependencies. In R, we use [`renv`](https://rstudio.github.io/renv/articles/renv.html).
To install these dependency managers, you can run (assumes Mac or Linux; see tools' documentation for other operating systems):

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
Rscript -e 'if(!requireNamespace("remotes")){install.packages("remotes");remotes::install_github("rstudio/renv")} else {remotes::install_github("rstudio/renv")}'
```

Once these are installed, you can install all dependencies with

```bash
poetry install
Rscript -e 'renv::restore()'
```

### Census API

In order to run some of this code, you will also need a [Census API Key](https://api.census.gov/data/key_signup.html). Once you have the key, copy the `.env.sample` file to `.env` and fill in your API key in the specified location.

## Replicating the analysis

To replicate the final analysis, run `make all`.

## Code layout

Use this section to describe your code layout.

## Tests

Several tests have been written in the `tests` folder. They may be run with `poetry run py.test`.

## License

MIT
