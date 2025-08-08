import numpy as np
import pandas as pd

from src.checks.check import Check
from src.types import GenericResponse


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

        return GenericResponse(
            type="computational",
            col=[self.formula, self.expected_result],
            wrong=len(bad_ids),
            missing=0,  # todo check
            total=len(df),
            bad_id_list=bad_ids,
        )
