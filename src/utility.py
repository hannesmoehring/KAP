import json
from typing import Tuple

import pandas as pd


# @return valid, invalid
def split_by_index(df: pd.DataFrame, index_list: list[int]) -> tuple[pd.DataFrame, pd.DataFrame]:
    index_set = set(index_list)
    mask = df.index.isin(index_set)

    invalid_df = df[mask]
    valid_df = df[~mask]

    return valid_df, invalid_df


def generate_df_overview_json(df: pd.DataFrame, file_name: str):
    overview = {}

    for col in df.columns:
        col_info = {"col_type": str(df[col].dtype)}

        unique_vals = df[col].dropna().unique()
        if len(unique_vals) <= 15:
            col_info["unique_values"] = [str(v) for v in unique_vals]

        overview[col] = col_info

    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(overview, f, indent=2)  # , ensure_ascii=False


# create a overview for each health metric and DQ metric with entries like this:  (% valid, % present)
def generate_2D_df_overview(df: pd.DataFrame) -> pd.DataFrame:
    result = []

    for col in df.columns:
        col_data = df[col]
        n_total = len(col_data)
        n_present = col_data.notna().sum()

        value_conform_flags = ...  # check_value_conform_range1(df[[col]])

        valid_present = (
            value_conform_flags[col].sum()
            if isinstance(value_conform_flags, pd.DataFrame)
            else value_conform_flags.sum()
        )
        pct_valid = valid_present / n_present if n_present > 0 else 0.0
        pct_present = n_present / n_total

        is_unique = df[col].dropna().duplicated().any() is False
        pct_unique = 1.0 if is_unique else 0.0

        result.append(
            {
                "variable": col,
                "value_conform": (round(pct_valid, 3), round(pct_present, 3)),
                "unique": (pct_unique, round(pct_present, 3)),
            }
        )

    return pd.DataFrame(result).set_index("variable")


# create an overview for each row, with DQ metrics at the top to see if row is unique or if row has missing values or how many values that dont conform
def generate_2D_row_overview(df: pd.DataFrame) -> pd.DataFrame:
    result = {}

    value_conform_flags = pd.DataFrame(False, index=df.index, columns=df.columns)

    duplicated_mask = df.apply(lambda col: col.duplicated(keep=False))
    unique_flags = ~duplicated_mask

    temporal_flags = pd.DataFrame(True, index=df.index, columns=df.columns)

    present_flags = df.notna()

    for idx in df.index:
        n_total = present_flags.loc[idx].sum()

        # Avoid division by zero for completely empty rows
        result[idx] = {
            "value_conform": (
                (value_conform_flags.loc[idx] & present_flags.loc[idx]).sum() / n_total if n_total else 0.0
            ),
            "unique": (unique_flags.loc[idx] & present_flags.loc[idx]).sum() / n_total if n_total else 0.0,
            "temporal_plausibility": (
                (temporal_flags.loc[idx] & present_flags.loc[idx]).sum() / n_total if n_total else 0.0
            ),
            "presence": n_total / df.shape[1],
        }

    return pd.DataFrame.from_dict(result, orient="index")
