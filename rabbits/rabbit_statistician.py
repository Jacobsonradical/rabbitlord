import polars as pl


def classification_index(dataframe, real_col, pred_col):
    if not dataframe[real_col].is_in([0, 1]).all():
        raise ValueError("The column with ground truth must be coded as 0 and 1 only!")

    if not dataframe[pred_col].is_in([0, 1]).all():
        raise ValueError("The column with predicted label must be coded as 0 and 1 only!")

    dataframe = dataframe.with_columns([
        ((pl.col(real_col) == 1) & (pl.col(pred_col) == 1)).alias("TP"),
        ((pl.col(real_col) == 0) & (pl.col(pred_col) == 1)).alias("FP"),
        ((pl.col(real_col) == 0) & (pl.col(pred_col) == 0)).alias("TN"),
        ((pl.col(real_col) == 1) & (pl.col(pred_col) == 0)).alias("FN"),
    ])

    metrics = dataframe.select([
        pl.sum("TP").alias("TP"),
        pl.sum("FP").alias("FP"),
        pl.sum("TN").alias("TN"),
        pl.sum("FN").alias("FN")
    ])

    tp, fp, tn, fn = metrics.row(0)

    accuracy = (tp + tn) / (tp + fp + tn + fn)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    if precision + recall == 0:
        raise Warning("The summation of Precision and Recall is zero. F1 score will be returned as 0.")
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return tp, fp, tn, fn, accuracy, precision, recall, f1
