import re
import os
from datetime import datetime
import glob
import polars as pl
from pathlib import Path


def sort_fps_date(list_fps, reverse=True):
    """
    :param list_fps: list of file paths
    :param reverse: True to sort backward, with the latest date the first.
    :return: sorted list of file paths
    """
    fps_sorted = sorted(list_fps,
                        key=lambda x: re.search(r"\d{4}-\d{2}-\d{2}", x).group(),
                        reverse=reverse)
    return fps_sorted


def extract_date(fp: str, position: int) -> str:
    """
    :position: 0 for basename, 1 for folder name, 2 for one more level higher folder name, and so on...

    The fname that requires to be parsed to get the must be of the format:
        {date}_something1_something2_something3_etc

    File extension: allowed.
    Length of _something_: any, including 0.
    {date} must appear first.
    """
    if position < 0:
        raise ValueError("Function argument `position` must be positive!")

    p = Path(fp).resolve()
    parts = [p.stem] + [part.name for part in p.parents]

    fname = parts[position]
    parts = fname.split("_")
    date = parts[0]
    return date


def cutoff_fps_date(list_fps, cutoff_start: str or None, cutoff_end: str or None, position: int):
    """
    :param position: 0 for basename, 1 for folder name, 2 for one more level higher folder name, and so on...
    :param list_fps: list of file paths
    :param cutoff_start: date string YYYY-MM-DD (will be excluded)
    :param cutoff_end: date string YYYY-MM-DD (will be included as the final date)
    :return: list of file paths
    """
    if position < 0:
        raise ValueError("Function argument `position` must be positive!")

    fps_cutoff = []
    for fp in list_fps:
        date = extract_date(fp, position)
        date_dt = datetime.strptime(date, "%Y-%m-%d")
        if (cutoff_start is None or date_dt > datetime.strptime(cutoff_start, "%Y-%m-%d")) and \
                (cutoff_end is None or date_dt <= datetime.strptime(cutoff_end, "%Y-%m-%d")):
            fps_cutoff.append(fp)
    return fps_cutoff












