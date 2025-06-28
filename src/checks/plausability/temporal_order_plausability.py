from src.checks.check import Check
from dataclasses import dataclass

import pandas as pd


class TemporalOrderPlausability(Check):

    def __init__(self,      
        col_1: str,
        col_2: str,
        inclusive: bool = True,
        allow_na: bool = False,
    ):
        self.column_1 = col_1
        self.column_2 = col_2
        self.inclusive = inclusive
        self.allow_na = allow_na


    def run_check(self, df):
        col_1 = self.column_1.strip()
        col_2 = self.column_2.strip()

        if col_1 not in df.columns or col_2 not in df.columns:
            raise Exception(f"Missing column: '{col_1}' or '{col_2}'")

        earlier = pd.to_datetime(df[col_1], errors="coerce", dayfirst=True)
        later = pd.to_datetime(df[col_2], errors="coerce", dayfirst=True)

        missing_mask = earlier.isna() | later.isna()

        if self.inclusive:
            bad_mask = later < earlier
        else:
            bad_mask = later <= earlier

        if not self.allow_na:
            bad_mask |= missing_mask

        bad_rows = df.index[bad_mask].tolist()

        return ResponseVCDateOrder(earlier=(later < earlier).sum(), missing=missing_mask.sum(), total=len(df), bad_id_list=bad_rows)
    

@dataclass
class ResponseVCDateOrder():
    earlier: int
    missing: int
    total: int
    bad_id_list: list[int]