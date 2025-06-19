from atomicwrites import atomic_write
import json
import os
import orjson


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

