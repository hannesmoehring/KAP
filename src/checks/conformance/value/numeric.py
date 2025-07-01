from src.checks.check import Check
from dataclasses import dataclass


class NumericValueConformanceCheck(Check):

    def __init__(self, col: str, min: float, max: float, inclusive: bool = True, allow_na: bool = False) :
        self.col = col
        self.min = min
        self.max = max
        self.inclusive = inclusive
        self.allow_na = allow_na

     
    def run_check(self, df):
        if self.col not in df.columns:
            raise Exception("no such column.")

        bad_rows = list[int]
        data = df[self.col]

        if self.inclusive:
            below_mask = data < min
            above_mask = data > max
            in_range = (data >= min) & (data <= max)
        else:
            below_mask = data <= min
            above_mask = data >= max
            in_range = (data > min) & (data < max)

        missing_mask = data.isna()

        bad_mask = below_mask | above_mask
        if not self.allow_na:
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


@dataclass
class ResponseVCNum():
    min: float
    max: float
    above: int
    below: int
    missing: int
    total: int
    bad_id_list: list[int]