import random
from datetime import datetime, timedelta
from typing import Literal, Union

import numpy as np
import pandas as pd



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


n_rows = 1000

columns = {
    "GBDAT_EXP_ADD": {"dtype": "date", "prob_bad": 0.2, "date_range": ("01.01.1950", "01.01.2025")},
    "GSCHL_EXP_ADD": {"dtype": "category", "values": ["w", "m", "F"], "prob_bad": 0.15},
    "ZNLMSVEDPY": {
        "dtype": "ordinal",
        "values": ["0", "1", "2", "3a", "3b", "4a", "4b", "4c", "5a", "5b", "5c"],
        "prob_bad": 0.25,
    },
    "ZNLMSVAEDA": {
        "dtype": "date",
        "prob_bad": 0.2,
        "date_range": ("01.01.1950", "01.01.2025"),
    },
}


def routine() -> pd.DataFrame:
    df_data = {}

    for col, config in columns.items():
        dtype = config["dtype"]
        prob_bad = config.get("prob_bad", 0.1)
        values = config.get("values", [])
        date_range = config.get("date_range", ("01.01.2000", "01.01.2025"))

        df_data[col] = generate_column_data(
            dtype=dtype, values=values, size=n_rows, prob_bad=prob_bad, date_range=date_range
        )
    
    df_data["ZNLMSVAGRO"] = np.random.normal(loc=170, scale=10, size=n_rows)
    df_data["ZNLMSVAGEW"] = np.random.normal(loc=70, scale=20, size=n_rows)

    df_data["ZNLMSVABMI"] = df_data["ZNLMSVAGEW"] / (df_data["ZNLMSVAGRO"] * df_data["ZNLMSVAGRO"] ) + np.random.random(n_rows)

    df = pd.DataFrame(df_data)
    return df
