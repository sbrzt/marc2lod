# main.py

import yaml
from pathlib import Path
from src.extract import extract_records
from src.transform import parse_records
from src.load import load_records


def main():

    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    records = extract_records(
        config["source"], 
        config["source_type"]
        )

    df = parse_records(records, config["fields"])

    load_records(df, config, Path("output"), config["outputs"])

if __name__ == "__main__":
    main()