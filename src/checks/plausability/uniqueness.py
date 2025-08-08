import pandas as pd

from src.checks.check import Check
from src.types import GenericResponse


class UniquenessPlausability(Check):
    def run_check(self, df) -> GenericResponse:
        # check for unique rows in the DataFrame
        unique_rows = df.drop_duplicates()
        total_rows = len(df)
        unique_count = len(unique_rows)
        non_unique_count = total_rows - unique_count
        non_unique_rows = df[df.duplicated(keep=False)]
        missing_count = df.isna().sum().sum()

        return GenericResponse(
            type="uniqueness",
            col=[],
            wrong=non_unique_count,
            total=total_rows,
            missing=missing_count,
            bad_id_list=non_unique_rows.index.tolist(),
        )
