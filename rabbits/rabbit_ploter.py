import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Union, Optional
import matplotlib.cm as cm


def prepare_stats(
        data: Dict[str, Union[np.ndarray, List[float], Tuple[float, float, int]]]
) -> Tuple[List[str], np.ndarray, np.ndarray, np.ndarray]:
    """
    The data must be preprocessed into either of the following three forms, I show them as examples.

    data = {
        "BLACK":        df_black.filter(pl.col("ifTrain") == 0)["answer"].to_numpy(),
        "BLACK train":  df_black.filter(pl.col("ifTrain") == 1)["answer"].to_numpy(),
        "WHITE":        df_white.filter(pl.col("ifTrain") == 0)["answer"].to_numpy(),
        "CONTROL":      df_control.filter(pl.col("ifTrain") == 0)["answer"].to_numpy(),
    }


    data = {
        "BLACK":        df_black.filter(pl.col("ifTrain") == 0)["answer"].to_list(),
        "BLACK train":  df_black.filter(pl.col("ifTrain") == 1)["answer"].to_list(),
        "WHITE":        df_white.filter(pl.col("ifTrain") == 0)["answer"].to_list(),
        "CONTROL":      df_control.filter(pl.col("ifTrain") == 0)["answer"].to_list(),
    }


    data = {
        "BLACK":       (mean_black_0, sd_black_0, n_black_0),
        "BLACK train": (mean_black_1, sd_black_1, n_black_1),
        "WHITE":       (mean_white_0, sd_white_0, n_white_0),
        "CONTROL":     (mean_control_0, sd_control_0, n_control_0),
    }
    """

    labels, means, sds, ns = [], [], [], []
    for label, value in data.items():
        if isinstance(value, tuple) and len(value) == 3:
            m, sd, n = value
        else:
            arr = np.asarray(value, dtype=float)
            arr = arr[~np.isnan(arr)]
            n = int(arr.size)
            m = float(arr.mean()) if n > 0 else np.nan
            sd = float(arr.std(ddof=1)) if n > 1 else np.nan
        labels.append(label)
        means.append(m)
        sds.append(sd)
        ns.append(n)
    return labels, np.array(means, float), np.array(sds, float), np.array(ns, int)


def plot_means_with_ci(
        data: Dict[str, Union[np.ndarray, List[float], Tuple[float, float, int]]],
        order: Optional[List[str]] = None,
        title: str = "",
        subtitle: Optional[str] = None,
        y_label: str = "",
        ylim: Optional[Tuple[float, float]] = (0.0, 1.0),
        ci_multiplier: float = 1.96,  # 95% CI
        capsize: float = 5.0,
        annotate: bool = True,
        rotation: int = 10,
        figsize: Tuple[int, int] = (8, 6),
        save_path: Optional[str] = None,
        show: bool = True,
):
    """

    :param data:
    :param order:
    :param title:
    :param subtitle:
    :param y_label:
    :param ylim:
    :param ci_multiplier:
    :param capsize:
    :param annotate:
    :param rotation:
    :param figsize:
    :param save_path:
    :param show:
    :return:
    """
    labels, means, sds, ns = prepare_stats(data)

    # Reorder if requested
    if order is not None:
        idx_map = {lbl: i for i, lbl in enumerate(labels)}
        ordered_idx = [idx_map[lbl] for lbl in order if lbl in idx_map]
        labels = [labels[i] for i in ordered_idx]
        means = means[ordered_idx]
        sds = sds[ordered_idx]
        ns = ns[ordered_idx]

    # CI half-widths (0 if n<=1 or sd is nan)
    ci_half = np.zeros_like(means, dtype=float)
    valid = (ns > 1) & (~np.isnan(sds)) & (~np.isnan(means))
    ci_half[valid] = ci_multiplier * (sds[valid] / np.sqrt(ns[valid]))

    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=figsize)

    # Bars + error bars
    cmap = plt.get_cmap("tab10")
    colors = [cmap(i % cmap.N) for i in range(len(labels))]
    rects = ax.bar(x, means, yerr=ci_half, capsize=capsize, color=colors)

    # Labels & axes
    main_title = title if subtitle is None else f"{title}\n{subtitle}"
    if main_title:
        ax.set_title(main_title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=rotation)
    ax.set_ylabel(y_label)
    if ylim is not None:
        ax.set_ylim(*ylim)

    # Optional annotations inside/above bars
    if annotate:
        y_min, y_max = ax.get_ylim()
        y_span = y_max - y_min
        for rect, m, n in zip(rects, means, ns):
            height = rect.get_height()
            # Place slightly above the bar top (works regardless of y-limits)
            y_pos = height + 0.02 * y_span
            text = f"n={n}\nMean={m:.3f}" if not np.isnan(m) else f"n={n}\nMean=NA"
            ax.text(
                rect.get_x() + rect.get_width() / 2.0,
                y_pos,
                text,
                ha="center",
                va="bottom",
                fontsize=8,
            )

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=120)
    if show:
        plt.show()
    plt.close(fig)
