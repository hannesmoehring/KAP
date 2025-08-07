import pandas as pd

from src.checks.check import Check
from src.types import GenericResponse


class TemporalValueConformance(Check):

    def __init__(self, col: str, min_date, max_date, inclusive: bool = False, allow_na: bool = False):
        self.col = col
        self.min_date = min_date
        self.max_date = max_date
        self.inclusive = inclusive
        self.allow_na = allow_na

    def run_check(self, df):
        self.col = self.col.strip()
        if self.col not in df.columns:
            raise Exception(f"no such column: '{self.col}'")

        try:
            data = pd.to_datetime(df[self.col], dayfirst=True, errors="coerce")
        except Exception as e:
            raise ValueError(f"could not convert column '{self.col}' to datetime: {e}")

        if self.inclusive:
            in_range_mask = (data >= self.min_date) & (data <= self.max_date)
            before_mask = data < self.min_date
            after_mask = data > self.max_date
        else:
            in_range_mask = (data > self.min_date) & (data < self.max_date)
            before_mask = data <= self.min_date
            after_mask = data >= self.max_date

        missing_mask = data.isna()

        if not self.allow_na:
            bad_mask = ~in_range_mask | missing_mask
        else:
            bad_mask = ~in_range_mask

        bad_rows = df.index[bad_mask].tolist()

        return GenericResponse(
            type="value_temporal",
            col=[self.col],
            wrong=bad_mask.sum(),
            missing=missing_mask.sum(),
            total=len(data),
            bad_id_list=bad_rows,
        )
