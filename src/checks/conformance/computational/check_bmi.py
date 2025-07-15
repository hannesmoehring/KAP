from src.checks.check import Check
from dataclasses import dataclass

import pandas as pd
import numpy as np

class BMICheck(Check):

    def __init__(self, height_column, weigh_column, bmi_column):
        self.height_column = height_column
        self.weigh_column = weigh_column
        self.bmi_column = bmi_column

    def run_check(self, df: pd.DataFrame, error: float = 0.1, allow_na=False):
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

        return ResponseBMI(
            wrong=invalid_mask,
            missing=missing_mask.sum(),
            total=len(df),
            bad_id_list=bad_ids,
        )


@dataclass
class ResponseBMI():
    wrong: int
    missing: int
    total: int
    bad_id_list: list[int]
