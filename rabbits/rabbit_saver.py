from atomicwrites import atomic_write
import json
import os
import orjson
import polars as pl
from rabbit_loader import load_dataframe


def save_extend(output_fp, list_extend, show_emoji=False):
    if os.path.exists(output_fp):
        with open(output_fp, "rt") as f:
            list_exist = json.load(f)
    else:
        list_exist = []
    list_exist.extend(list_extend)
    with atomic_write(output_fp, overwrite=True) as f:
        json.dump(list_exist, f, ensure_ascii=not show_emoji)


def save_append(output_fp, to_append, show_emoji=False):
    if os.path.exists(output_fp):
        with open(output_fp, "rt") as f:
            list_exist = json.load(f)
    else:
        list_exist = []
    list_exist.append(to_append)
    with atomic_write(output_fp, overwrite=True) as f:
        json.dump(list_exist, f, ensure_ascii=not show_emoji)


def fast_save_json(output_fp, data):
    with open(output_fp, "wb") as f:
        f.write(orjson.dumps(data))


def save_dataframe(
        output_fp,
        dataframe: pl.DataFrame,
):
    _, ext = os.path.splitext(output_fp)
    if ext not in {".csv", ".tsv", ".parquet", ".json"}:
        raise ValueError(f"Unsupported file type: {ext}.")
    elif ext == ".csv":
        dataframe.write_csv(output_fp)
    elif ext == ".tsv":
        dataframe.write_csv(output_fp, separator="\t")
    elif ext == ".parquet":
        dataframe.write_parquet(output_fp)
    else:
        dataframe.write_json(output_fp)


def save_concat(
        output_fp,
        data: pl.DataFrame
):
    if os.path.exists(output_fp):
        df_exist = load_dataframe(output_fp)
        df = pl.concat([df_exist, data], how="vertical")
    else:
        df = data
    save_dataframe(output_fp, df)

