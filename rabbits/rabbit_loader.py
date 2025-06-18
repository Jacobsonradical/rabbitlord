import polars as pl
import os
import zipfile
import orjson


def load_dataframe(fp):
    _, ext = os.path.splitext(fp)
    if ext not in {".zip", ".csv", ".tsv", ".json", ".parquet"}:
        raise ValueError(f"Unsupported file type: {ext}.")
    elif ext == ".zip":
        with zipfile.ZipFile(fp, 'r') as z:
            if len(z.namelist()) != 1:
                raise ValueError("You have multiple files in the zip.")

            inner_file = z.namelist()[0]
            inner_ext = os.path.splitext(inner_file)[1].lower()
            if inner_ext not in {".csv", ".tsv", ".json"}:
                raise ValueError(f"Unsupported inner file type in zip: {ext}.")

            with z.open(inner_file) as f:
                if inner_ext == ".csv":
                    df = pl.read_csv(f)
                elif inner_ext == ".tsv":
                    df = pl.read_csv(f, separator="\t")
                elif inner_ext == ".json":
                    df = pl.read_json(f)
                else:
                    df = pl.read_parquet(f)
    elif ext == ".csv":
        df = pl.read_csv(fp)
    elif ext == ".tsv":
        df = pl.read_csv(fp, separator="\t")
    elif ext == ".parquet":
        df = pl.read_parquet(fp)
    else:
        df = pl.read_json(fp)
    return df


def fast_load_json(fp):
    with open(fp, "rb") as f:
        json_data = orjson.loads(f.read())
    return json_data

