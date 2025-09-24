import polars as pl
import math


def safe_div(n, d):
    return n / d if d != 0 else float("nan")


def f_beta(beta, precision, recall):
    if math.isnan(precision) or math.isnan(recall):
        return float("nan")
    if (precision + recall) == 0:
        return 0.0
    b2 = beta * beta
    return safe_div((1 + b2) * precision * recall, (b2 * precision) + recall)


def classification_index(
        dataframe: pl.DataFrame,
        real_col: str,
        pred_col: str,
        beta_values: tuple[float, ...] = (0.5, 1.0, 2.0),
):
    """
    Compute confusion-matrix metrics for a binary classifier (0/1 labels).
    Parameters
    ----------
    dataframe : pl.DataFrame
        Must contain the ground-truth and predicted-label columns (coded as 0/1).
    real_col : str
        Name of ground-truth column (0/1).
    pred_col : str
        Name of predicted-label column (0/1).
    beta_values : tuple[float, ...]
        Beta values for F-beta scores to report (e.g., 0.5 emphasizes precision, 2 emphasizes recall).

    Returns
    -------
    dict
        Dictionary of metrics (ints/floats), robust to division-by-zero.
    """
    if not dataframe[real_col].is_in([0, 1]).all():
        raise ValueError("The column with ground truth must be coded as 0/1 only.")
    if not dataframe[pred_col].is_in([0, 1]).all():
        raise ValueError("The column with predicted label must be coded as 0/1 only.")

    df = dataframe.with_columns([
        ((pl.col(real_col) == 1) & (pl.col(pred_col) == 1)).alias("_TP"),
        ((pl.col(real_col) == 0) & (pl.col(pred_col) == 1)).alias("_FP"),
        ((pl.col(real_col) == 0) & (pl.col(pred_col) == 0)).alias("_TN"),
        ((pl.col(real_col) == 1) & (pl.col(pred_col) == 0)).alias("_FN"),
    ])

    metrics_df = df.select([
        pl.sum("_TP").alias("TP"),
        pl.sum("_FP").alias("FP"),
        pl.sum("_TN").alias("TN"),
        pl.sum("_FN").alias("FN"),
        pl.len().alias("N"),
    ])
    tp, fp, tn, fn, n = metrics_df.row(0)

    # Core rates
    accuracy = safe_div(tp + tn, n)
    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    specificity = safe_div(tn, tn + fp)  # Out of all the actual negatives, how many did the classifier correctly predict as negative?
    fpr = safe_div(fp, fp + tn)  # Out of all the actual negatives, how many did the classifier incorrectly predict as positive?
    fnr = safe_div(fn, fn + tp)  # Out of all the actual positives, how many did the classifier miss?
    npv = safe_div(tn, tn + fn)  # Out of all the predicted negatives, how many are actually negative
    prevalence = safe_div(tp + fn, n)  # The proportion of the dataset that is actually positive.

    # Balanced accuracy & Youden's J
    balanced_accuracy = (recall + specificity) / 2 if not (math.isnan(recall) or math.isnan(specificity)) else float(
        "nan")
    youdens_j = (recall + specificity - 1) if not (math.isnan(recall) or math.isnan(specificity)) else float("nan")

    f1 = f_beta(1.0, precision, recall)
    f_betas = {f"f{str(beta).replace('.', '_')}": f_beta(beta, precision, recall) for beta in beta_values if beta != 1.0}

    mcc_denominator = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    mcc = safe_div(tp * tn - fp * fn, mcc_denominator)  # Matthews Correlation Coefficient

    out = {
        "prevalence": prevalence,
        "TP": int(tp),
        "FP": int(fp),
        "TN": int(tn),
        "FN": int(fn),
        "N": int(n),
        "accuracy": accuracy,
        "balanced_accuracy": balanced_accuracy,
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "npv": npv,
        "fpr": fpr,
        "fnr": fnr,
        "f1": f1,
        **f_betas,
        "youden_j": youdens_j,
        "mcc": mcc,
    }

    return out
