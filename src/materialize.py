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
    
    context = {**uri_patterns, **row.to_dict()}
    subject_uri = uri_patterns["subject_uri"].format(**context)
    subject_class = field_conf.get("subject_class")
    if subject_class:
        triples.append((
            URIRef(subject_uri),
            URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
            URIRef(subject_class),
        ))
    
    value = row.get(field_name)
    if value is None:
        return triples
    templates = field_conf.get("mapping", {}).get("template", [])
    if isinstance(value, list):
        values = [v for v in value if v is not None and not pd.isna(v)]
        if not values:
            return triples
    else:
        if pd.isna(value):
            return triples
        values = [value]

    for idx, val in enumerate(values):
        if field_conf.get("mapping", {}).get("uri_strategy") == "global":
            object_uri = field_conf["mapping"]["uri_pattern"].format(
                base_uri=uri_patterns["base_uri"],
                normalized_value=normalize_uri(val),
                **row.to_dict()
            )
        else:
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
            datatype = template.get("datatype")
            if is_uri(obj_val):
                obj = URIRef(generate_uri(obj_val, prefixes))
            else:
                if datatype:
                    obj = Literal(obj_val, datatype=URIRef(generate_uri(datatype, prefixes)))
            triples.append((subj, pred, obj))
    return triples


def normalize_uri(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^\w]+", "-", value)
    value = value.strip("-")
    return value


def materialize(
    df, 
    config
    ):

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
        