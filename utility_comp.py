import numpy as np
import pandas as pd

from types_kap import *


# bmi: kg / (height in meter)^2
def check_computational_conformance_bmi(df: pd.DataFrame, error: float = 0.1, allow_na=False):
    height: float = pd.to_numeric(df["ZNLMSVAGRO"], errors="coerce") / 100
    weight: float = pd.to_numeric(df["ZNLMSVAGEW"], errors="coerce")
    bmi: float = pd.to_numeric(df["ZNLMSVABMI"], errors="coerce")

    missing_mask = height.isna() | weight.isna() | bmi.isna()

    expected_bmi: float = weight / (height**2)

    diff = np.abs(expected_bmi - bmi)
    invalid_mask = diff > error

    if not allow_na:
        bad_mask = missing_mask | invalid_mask
    else:
        bad_mask = invalid_mask

    bad_ids = df.index[bad_mask].tolist()

    return ResponseCC(
        wrong=invalid_mask,
        missing=missing_mask.sum(),
        total=len(df),
        bad_id_list=bad_ids,
    )
