# Value Conformance Utility

import pandas as pd

from types_kap import *


def check_value_conformance_numeric(
    col: str,
    min: float,
    max: float,
    df: pd.DataFrame,
    inclusive: bool = True,
    allow_na: bool = False,
) -> ResponseVCNum:
    if col.strip() not in df.columns:
        raise Exception("no such column.")

    bad_rows = list[int]
    data = df[col]

    if inclusive:
        below_mask = data < min
        above_mask = data > max
        in_range = (data >= min) & (data <= max)
    else:
        below_mask = data <= min
        above_mask = data >= max
        in_range = (data > min) & (data < max)

    missing_mask = data.isna()

    bad_mask = below_mask | above_mask
    if not allow_na:
        bad_mask |= missing_mask

    # TODO, get id or something for the bad entries
    bad_rows = df.index[bad_mask].tolist()

    return ResponseVCNum(
        min=in_range.min(skipna=True),
        max=in_range.max(skipna=True),
        above=above_mask.sum(),
        below=below_mask.sum(),
        missing=missing_mask.sum(),
        total=len(data),
        bad_id_list=bad_rows,
    )


def check_value_conformance_string(
    col: str, allowed_strings: list[str], df: pd.DataFrame, allow_na: bool = False
) -> ResponseVCStr:
    if col.strip() not in df.columns:
        raise Exception("no such column.")

    bad_rows = list[int]
    data = df[col]
    missing_mask = data.isna()
    outside_mask = ~data.isin(allowed_strings) & ~missing_mask

    if not allow_na:
        bad_mask = outside_mask | missing_mask
    else:
        bad_mask = outside_mask

    bad_rows = df.index[bad_mask].tolist()

    return ResponseVCStr(outside=outside_mask.sum(), missing=missing_mask.sum(), total=len(data), bad_id_list=bad_rows)


def check_value_conformance_temporal(
    col: str,
    df: pd.DataFrame,
    min_date: pd.Timestamp,
    max_date: pd.Timestamp = pd.Timestamp("2025-01-01"),
    inclusive: bool = False,
    allow_na: bool = False,
) -> ResponseVCDate:

    col = col.strip()
    if col not in df.columns:
        raise Exception(f"no such column: '{col}'")

    try:
        data = pd.to_datetime(df[col], errors="coerce")
    except Exception as e:
        raise ValueError(f"could not convert column '{col}' to datetime: {e}")

    if inclusive:
        in_range_mask = (data >= min_date) & (data <= max_date)
        before_mask = data < min_date
        after_mask = data > max_date
    else:
        in_range_mask = (data > min_date) & (data < max_date)
        before_mask = data <= min_date
        after_mask = data >= max_date

    missing_mask = data.isna()

    if not allow_na:
        bad_mask = ~in_range_mask | missing_mask
    else:
        bad_mask = ~in_range_mask

    bad_rows = df.index[bad_mask].tolist()

    return ResponseVCDate(before=before_mask.sum(), after=after_mask.sum(), total=len(data), bad_id_list=bad_rows)
