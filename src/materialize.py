# src/materialize.py

import re
import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace


def generate_uri(
    uri,
    prefixes
    ):
    if uri.startswith("http://") or uri.startswith("https://"):
        return uri
    if ":" not in uri:
        raise ValueError(f"Not a URI")
    prefix, local = uri.split(":", 1)
    if prefix not in prefixes:
        raise KeyError(f"Unknown prefix: {prefix}")
    return prefixes[prefix] + local

def is_uri(value):
    if not isinstance(value, str):
        return False
    return bool(re.match(r"^https?://", value))


def generate_triples(
    row,
    field_name,
    field_conf,
    prefixes,
    uri_patterns
    ):

    triples = []
    value = row.get(field_name)
    if pd.isna(value):
        return triples

    templates = field_conf.get("mapping", {}).get("template", [])
    
    if isinstance(value, list):
        values = value
    else:
        values = [value]
    
    subject_uri = uri_patterns["subject_uri"].format(**row.to_dict())

    for idx, val in enumerate(values):
        object_uri = uri_patterns["object_uri"].format(
            subject_uri=subject_uri,
            field=field_name.lower(),
            index=idx,
            **row.to_dict()
        )
        for template in templates:
            context = {
                **row.to_dict(),
                "subject_uri": subject_uri,
                "object_uri": object_uri,
                "value": val,
                "field": field_name.lower(),
                "index": idx
            }
        
            subj = URIRef(generate_uri(template["subject"].format(**context), prefixes))
            pred = URIRef(generate_uri(template["predicate"].format(**context), prefixes))
            obj_val = template["object"].format(**context)
            if is_uri(obj_val):
                obj = URIRef(generate_uri(obj_val, prefixes))
            else:
                obj = Literal(obj_val)

            triples.append((subj, pred, obj))
    return triples


def materialize(df, config):
    g = Graph()

    for prefix, uri in config.get("prefixes", {}).items():
        if uri:
            g.bind(prefix, Namespace(uri))

    uri_patterns = config.get("uri_patterns", {})

    for _, row in df.iterrows():
        for field_name, field_conf in config["fields"].items():
            triples = generate_triples(row, field_name, field_conf, config["prefixes"], uri_patterns)
            for triple in triples:
                g.add(triple)
    return g
        