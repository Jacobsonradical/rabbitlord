from atomicwrites import atomic_write
import json
import os


def save_extend(output_fp, list_extend):
    if os.path.exists(output_fp):
        with open(output_fp, "rt") as f:
            list_exist = json.load(f)
    else:
        list_exist = []
    list_exist.extend(list_extend)
    with atomic_write(output_fp, overwrite=True) as f:
        json.dump(list_exist, f)


def save_append(output_fp, to_append):
    if os.path.exists(output_fp):
        with open(output_fp, "rt") as f:
            list_exist = json.load(f)
    else:
        list_exist = []
    list_exist.append(to_append)
    with atomic_write(output_fp, overwrite=True) as f:
        json.dump(list_exist, f)


