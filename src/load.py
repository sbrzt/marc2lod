# src/load.py

import pandas as pd
from pathlib import Path
from rdflib import Graph
from src.materialize import materialize


def save_rdf(
    graph: Graph,
    output_path: Path,
    serialization: str = "ttl"
    ) -> None:

    graph.serialize(destination=str(output_path), format=serialization)
    print(f"RDF saved to {output_path} [{serialization}]")

def save_table(
    df: pd.DataFrame,
    output_path: Path,
    fmt: str = "csv",
    exclude_fields: list | None = None
    ):

    if exclude_fields:
        df = df.drop(columns=[c for c in exclude_fields if c in df.columns])

    if fmt == "csv":
        df.to_csv(output_path, index=False)
    elif fmt == "xlsx":
        df.to_excel(output_path, index=False)
    elif fmt == "json":
        df.to_json(output_path, orient="records", lines=True)
    else:
        raise ValueError(f"unsupported table format: {fmt}")
    print(f"Table saved to {output_path} [{fmt}]")

def load_records(
    df: pd.DataFrame,
    config: dict,
    output_path: Path,
    outputs: list
    ):

    output_path.mkdir(parents=True, exist_ok=True)
    for output in outputs:
        kind = output["type"]
        if kind == "rdf":
            g = materialize(df, config)
            ext = output.get("format", "ttl")
            path = output_path / f"data.{ext}"
            save_rdf(g, path, ext)
        elif kind == "table":
            ext = output.get("format", "csv")
            exclude_fields = output.get("exclude_fields", [])
            path = output_path / f"data.{ext}"
            save_table(df, path, ext, exclude_fields)
    