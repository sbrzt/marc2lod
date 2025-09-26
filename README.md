---
title: marc2lod
tags:
    - data engineering
    - linked data engineering
    - bibliometrics
    - bibliographic data
    - etl pipeline
---

# marc2lod

## Description

This project provides a flexible prototype pipeline for **extracting, cleaning, and materializing MARCXML bibliographic data** into multiple output formats such as RDF, CSV, JSON, SQL, and more.  

It is designed for use cases where MARC records need to be transformed into structured datasets or knowledge graphs, with configurable mappings defined in a YAML file.

---

## Features

- **Extraction**
  - Read MARCXML from:
    - Local files (`.xml`)
    - Directories of files
    - Remote URLs
    - Raw XML strings
- **Transformation**
  - Apply configurable cleaning functions (regex replace, extract, normalization)
  - Support for multiple values per field (with configurable separators)
- **Materialization**
  - Generate RDF triples from MARC fields via mapping templates
  - Create unique, stable URIs with configurable strategies (`local` vs `global`)
- **Multiple outputs**
  - RDF (Turtle, RDF/XML, JSON-LD, N-Triples)
  - Tables (CSV, XLSX, JSON, SQL)
- **Configurable**
  - Controlled by a single `config.yaml` file
  - Define prefixes, URI patterns, field mappings, and outputs

---

## Project Structure

```
.
├── data/                       # Example MARCXML input files
├── output/                     # Generated outputs (RDF, CSV, etc.)
├── src/
│ ├── extract.py                # Fetching MARCXML records
│ ├── transform.py              # Data transformation into a unified DataFrame
│ ├── materialize.py            # RDF materialization based on config
│ ├── load.py                   # Output writers (RDF, tables, SQL, etc.)
│ └── clean.py                  # Helpers for data cleaning
├── tests/                      # Unit tests
├── config.yaml                 # User configuration
└── main.py                     # Entry point of the pipeline
```

---

## Usage

1. **Prepare your MARCXML data**  
Place one or more `.xml` files in the `data/` directory.

2. **Edit the config**  
Configure your `config.yaml` with:
- Source type (`file`, `url`, `string`)
- Source location (file path, directory, or URL)
- Output formats (rdf, csv, json, etc.)
- Prefixes, URI patterns, and field mappings

3. **Run the pipeline**

```bash
python main.py
```

4. **Check the outputs**
Results are written to the output/ folder.

---

## Roadmap

- [x] Support for large-scale corpora (e.g. Internet Archive collections)
- [] Research bundle generation: data in multiple formats + documentation
- [] CLI options for running with custom configs
- [] Report generation with basic stats and visualizations
- [] More cleaning functions
- [] Enrichment with external authority data (VIAF, Wikidata, etc.)


---

## Requirements

* Python 3.10+
* Dependencies:
  - pandas
  - rdflib
  - pymarc
  - requests
  - openpyxl

Install dependencies with:
```
pip install -r requirements.txt
```