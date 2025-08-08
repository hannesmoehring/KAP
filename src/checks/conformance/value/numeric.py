from src.checks.check import Check
from src.types import GenericResponse


class NumericValueConformanceCheck(Check):

    def __init__(self, col: str, min_val: float, max_val: float, inclusive: bool = True, allow_na: bool = False):
        self.col = col
        self.min_val = min_val
        self.max_val = max_val
        self.inclusive = inclusive
        self.allow_na = allow_na

    def run_check(self, df):
        if self.col not in df.columns:
            raise Exception("no such column.")

        bad_rows = list[int]
        data = df[self.col]

        if self.inclusive:
            below_mask = data < self.min_val
            above_mask = data > self.max_val
            in_range = (data >= self.min_val) & (data <= self.max_val)
        else:
            below_mask = data <= self.min_val
            above_mask = data >= self.max_val
            in_range = (data > self.min_val) & (data < self.max_val)

        missing_mask = data.isna()

        bad_mask = below_mask | above_mask
        if not self.allow_na:
            bad_mask |= missing_mask

        # TODO, get id or something for the bad entries
        bad_rows = df.index[bad_mask].tolist()

        return GenericResponse(
            type="value_numeric",
            col=[self.col],
            wrong=bad_mask.sum(),
            missing=missing_mask.sum(),
            total=len(data),
            bad_id_list=bad_rows,
        )
