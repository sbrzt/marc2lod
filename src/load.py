# src/load.py

import pandas as pd
import sqlite3
import zipfile
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
    exclude_fields: list | None = None,
    list_separator: str = "; "
    ):

    if exclude_fields:
        df = df.drop(columns=[c for c in exclude_fields if c in df.columns])

    df = df.map(lambda x: list_separator.join(map(str, x)) if isinstance(x, list) else x)

    if fmt == "csv":
        df.to_csv(output_path, index=False)
    elif fmt == "xlsx":
        df.to_excel(output_path, index=False)
    elif fmt == "json":
        df.to_json(output_path, orient="records", lines=True)
    elif fmt == "sql":
        conn = sqlite3.connect(output_path)
        df.to_sql("records", conn, if_exists="replace", index=False)
        conn.close()
    else:
        raise ValueError(f"unsupported table format: {fmt}")
    print(f"Table saved to {output_path} [{fmt}]")


def bundle_outputs(
    output_dir: Path,
    zip_name: str = "bundle.zip"
    ):

    zip_path = output_dir / zip_name
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in output_dir.rglob("*"):
            if file.is_file() and file != zip_path:
                zf.write(file, file.relative_to(output_dir))
    print(f"Bundle created at {zip_path}")
    return zip_path



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
            list_separator = output.get("list_separator", "; ")
            path = output_path / f"data.{ext}"
            save_table(df, path, ext, exclude_fields, list_separator)
    
    bundle_outputs(output_path)