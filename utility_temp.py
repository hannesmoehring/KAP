import pandas as pd

from types_kap import *


def check_temporal_order_plausibility(
    col_1: str,
    col_2: str,
    df: pd.DataFrame,
    inclusive: bool = False,
    allow_na: bool = False,
) -> ResponseVCDate:

    col_1 = col_1.strip()
    col_2 = col_2.strip()

    if col_1 not in df.columns or col_2 not in df.columns:
        raise Exception(f"Missing column: '{col_1}' or '{col_2}'")

    earlier = pd.to_datetime(df[col_1], errors="coerce", dayfirst=True)
    later = pd.to_datetime(df[col_2], errors="coerce", dayfirst=True)

    missing_mask = earlier.isna() | later.isna()

    if inclusive:
        bad_mask = later < earlier
    else:
        bad_mask = later <= earlier

    if not allow_na:
        bad_mask |= missing_mask

    bad_rows = df.index[bad_mask].tolist()

    return ResponseVCDateOrder(
        earlier=(later < earlier).sum(), missing=missing_mask.sum(), total=len(df), bad_id_list=bad_rows
    )
