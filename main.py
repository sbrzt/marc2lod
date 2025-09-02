# main.py

import yaml
from src.extract import extract_records

config_file = "config.yaml"

def main():
    config = yaml.safe_load(open(config_file))

    records = extract_records(
        config["source"], 
        config["source_type"]
        )

    print(records)

if __name__ == "__main__":
    main()