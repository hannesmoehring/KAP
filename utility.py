from typing import Tuple

import pandas as pd


def split_by_index(df: pd.DataFrame, index_list: list[int]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    index_set = set(index_list)
    mask = df.index.isin(index_set)

    invalid_df = df[mask]
    valid_df = df[~mask]

    return valid_df, invalid_df
