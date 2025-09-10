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
    