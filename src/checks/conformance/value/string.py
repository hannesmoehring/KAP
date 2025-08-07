from src.checks.check import Check
from src.types import GenericResponse


class StringValueConformance(Check):

    # todo: add case sensitivity option
    def __init__(self, col: str, allowed_strings: list[str], allow_na: bool = False):
        self.col = col
        self.allowed_strings = allowed_strings
        self.allow_na = allow_na

    def run_check(self, df):
        if self.col.strip() not in df.columns:
            raise Exception("no such column: {}".format(self.col))

        bad_rows = list[int]
        data = df[self.col]
        missing_mask = data.isna()
        outside_mask = ~data.isin(self.allowed_strings) & ~missing_mask

        if not self.allow_na:
            bad_mask = outside_mask | missing_mask
        else:
            bad_mask = outside_mask

        bad_rows = df.index[bad_mask].tolist()

        return GenericResponse(
            type="string_conformance",
            col=[self.col],
            wrong=bad_mask.sum(),
            missing=missing_mask.sum(),
            total=len(data),
            bad_id_list=bad_rows,
        )
