import json
import os
import random
from dataclasses import asdict, is_dataclass
from datetime import datetime, timedelta
from typing import Literal, Union

import numpy as np
import pandas as pd

from src.types import Result


def random_date(start: str, end: str, fmt="%d.%m.%Y") -> str:
    start_dt = datetime.strptime(start, fmt)
    end_dt = datetime.strptime(end, fmt)
    delta = (end_dt - start_dt).days
    rand_days = random.randint(0, delta)
    return (start_dt + timedelta(days=rand_days)).strftime(fmt)


def generate_column_data(
    dtype: Literal["date", "category", "ordinal"],
    values: Union[list[str], list[int]],
    size: int,
    prob_bad: float = 0.1,
    date_range: tuple = ("01.01.2000", "01.01.2025"),
    fmt="%d.%m.%Y",
) -> list:
    data = []
    for _ in range(size):
        is_bad = np.random.rand() < prob_bad
        is_bad_2 = np.random.rand() < prob_bad
        if dtype == "date":
            if is_bad:
                temp = random_date(start="01.01.1800", end="01.01.2050", fmt=fmt)
                data.append(random.choice(["32.13.2020", np.nan, temp]))

            else:
                data.append(random_date(*date_range, fmt=fmt))
        elif dtype == "category":
            if is_bad:
                data.append(random.choice(["invalid", "fw", "", np.nan]))
            else:
                data.append(random.choice(values))
        elif dtype == "ordinal":
            if is_bad:
                data.append(random.choice(["9", "9c", "1c", "unknown", np.nan]))
            else:
                data.append(random.choice(values))
    return data


N_ROWS = 1000

columns = {
    "GBDAT_EXP_ADD": {"dtype": "date", "prob_bad": 0.002, "date_range": ("01.01.1950", "01.01.2025")},
    "GSCHL_EXP_ADD": {"dtype": "category", "values": ["w", "m", "F"], "prob_bad": 0.01},
    "ZNLMSVEDPY": {
        "dtype": "ordinal",
        "values": ["0", "1", "2", "3a", "3b", "4a", "4b", "4c", "5a", "5b", "5c"],
        "prob_bad": 0.0003,
    },
    "ZNLMSVAEDA": {
        "dtype": "date",
        "prob_bad": 0.002,
        "date_range": ("01.01.1950", "01.01.2025"),
    },
}


def routine() -> pd.DataFrame:
    df_data = {}

    for col, config in columns.items():
        dtype = config["dtype"]
        prob_bad = config.get("prob_bad", 0.0001)
        values = config.get("values", [])
        date_range = config.get("date_range", ("01.01.2000", "01.01.2025"))

        df_data[col] = generate_column_data(dtype=dtype, values=values, size=N_ROWS, prob_bad=prob_bad, date_range=date_range)

    df_data["ZNLMSVAGRO"] = np.random.normal(loc=170, scale=10, size=N_ROWS)
    df_data["ZNLMSVAGEW"] = np.random.normal(loc=70, scale=20, size=N_ROWS)

    df_data["ZNLMSVABMI"] = df_data["ZNLMSVAGEW"] / (df_data["ZNLMSVAGRO"] * df_data["ZNLMSVAGRO"]) + np.random.random(N_ROWS)

    df = pd.DataFrame(df_data)
    return df


def dataclass_to_json(obj):
    if is_dataclass(obj):
        return {key: dataclass_to_json(value) for key, value in asdict(obj).items()}
    elif isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, list):
        return [dataclass_to_json(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: dataclass_to_json(value) for key, value in obj.items()}
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    else:
        return obj


def export_to_json(results: Result):
    os.makedirs("results", exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d_%H-%M")
    data = dataclass_to_json(results)
    with open(f"results/results_{date}.json", "w") as f:
        json.dump(data, f, indent=4)
    print(f"Results exported to results/results_{date}.json")


def infer_dtype(dtype):
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return "date"
    elif pd.api.types.is_integer_dtype(dtype):
        return "int64"
    elif pd.api.types.is_float_dtype(dtype):
        return "float64"
    elif dtype == "category":  # if less than 20 unique values, use category. should double check
        return "category"
    else:
        return "UNKNOWN"  # default to UNKNOWN for object/string


def generate_config_from_csv(csv_path: str, output_json_path: str):
    df = pd.read_csv(csv_path)

    for col in df.select_dtypes(include="object"):
        unique_vals = df[col].nunique(dropna=True)
        if unique_vals <= 20:
            df[col] = df[col].astype("category")

    config = {
        "columns": [],
        "parsers": [{"columns": [None], "mapping": None, "case_sensitive": None}],
        "checks": [
            {
                "type": None,
                "column": None,
                "values": None,
                "date_range": {"start": None, "end": None},
                "first": None,
                "last": None,
                "formula": None,
                "expected_result": None,
                "error": None,
            }
        ],
    }

    for col in df.columns:
        dtype = infer_dtype(df[col].dtype)

        col_entry = {"name": col, "dtype": dtype}

        if dtype in ["category", "ordinal"]:
            col_entry["values"] = None
        elif dtype in ["int64", "float64"]:
            col_entry["min"] = None
            col_entry["max"] = None

        config["columns"].append(col_entry)

    dir_name = os.path.dirname(output_json_path)

    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    with open(output_json_path, "w") as f:
        json.dump(config, f, indent=4)

    print(f"Template config saved to {output_json_path}")
