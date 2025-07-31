from src.checks.check import Check
from dataclasses import dataclass

import pandas as pd
import numpy as np

class ComputationalCheck(Check):

    def __init__(self, formula, expected_result, error=0):
        self.formula = formula
        self.expected_result = expected_result
        self.error = error

    def run_check(self, df: pd.DataFrame):

        result = df.eval(self.formula)

        diff = np.abs(result - df[self.expected_result])
        invalid_mask = diff > self.error

        bad_ids = df.index[invalid_mask].tolist()

        return ResponseComputational(
            wrong=invalid_mask,
            total=len(df),
            bad_id_list=bad_ids,
        )


@dataclass
class ResponseComputational():
    wrong: int
    total: int
    bad_id_list: list[int]
