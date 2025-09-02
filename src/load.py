# src/load.py

import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd


def save_to_parquet(
    df: pd.DataFrame,
    path: str
    ) -> None:

    collection = ia.get_item('darwinslibrary')

    metadata = {
        'identifier': f'{collection.metadata["identifier"]}',
        'title': f'{collection.metadata["title"]}',
        'description': f'{collection.metadata["description"]}',
        'creator': f'{collection.metadata["uploader"]}',
        'created': f'{collection.metadata["addeddate"]}',
        'subject': f'{collection.metadata["collection"]}',
        'source': f'{collection.metadata["identifier-access"]}'
    }

    # define unique key for custom metadata
    meta_key = 'darwinsarchive.iot'

    # use PyArrow to convert the DataFrame into an Arrow table
    table = pa.Table.from_pandas(df)

    # construct a new Arrow table that is a copy of `table`, 
    # but with its native metadata replaced by a combination of 
    # the existing metadata and our custom metadata
    meta_json = json.dumps(metadata)
    existing_meta = table.schema.metadata
    combined_meta = {
        meta_key.encode() : meta_json.encode(),
        **existing_meta
    }
    table = table.replace_schema_metadata(combined_meta)

    # save the Arrow table as a `.parquet` file by using the `parquet` library
    pq.write_table(table, '2024-01-16_darwinslibrary_v01.parquet', compression='GZIP')