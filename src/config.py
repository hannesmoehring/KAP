# Parse the config of the files
# Author: Bruno Scharlau, 28.06.2025
import json
import os

from src.checks.check import Check
from src.checks.conformance.computational.computational import ComputationalCheck
from src.checks.conformance.value.numeric import NumericValueConformanceCheck
from src.checks.conformance.value.string import StringValueConformance
from src.checks.conformance.value.temporal import TemporalValueConformance
from src.checks.plausability.temporal_order_plausability import (
    TemporalOrderPlausability,
)
from src.checks.plausability.uniqueness import UniquenessPlausability
from src.parsers.parser import Parser
from src.types import MAX_DATE, MIN_DATE


class Config:
    def __init__(self, config_path):
        if not config_path:
            raise ValueError("Set config.")

        if not os.path.isfile(config_path):
            raise FileNotFoundError(f"Couldn't find config file {config_path}. Are you sure the file exists?")

        self.config_path = config_path
        self.config_json = self._get_config()

    def _get_config(self) -> dict:
        with open(self.config_path, "r") as config_file:
            return json.loads("".join(config_file.readlines()))

    def _json_to_parser(self, json):
        return Parser(mapping=json["mapping"], columns=json["columns"], case_sensitive=json.get("case_sensitive", False))

    def _json_to_check(self, json):
        if "type" not in json.keys():
            raise KeyError("check_type not defined.")
        check_type = json["type"]

        if check_type == "temporal_value_conformance":
            return TemporalValueConformance(
                json["column"],
                json["date_range"]["start"],
                json["date_range"]["end"],
                json.get("inclusive", False),
                json.get("allow_na", False),
            )

        elif check_type == "string_value_conformance":
            return StringValueConformance(json["column"], json["values"], json.get("allow_na", False))

        elif check_type == "temporal_order_plausability":
            return TemporalOrderPlausability(json["first"], json["last"], json.get("inclusive", False), json.get("allow_na", False))

        elif check_type == "computational":
            return ComputationalCheck(json["formula"], json["expected_result"], json.get("error", 0))

        elif check_type == "numeric_value_conformance":
            return NumericValueConformanceCheck(json["column"], json["min"], json["max"], json.get("allow_na", False))

        else:
            raise RuntimeError(f"Check for type {check_type} not configured.")

    def get_json_config(self):
        return self.config_json

    def get_stage_1_checks(self) -> list[Check]:
        ret = []
        ret.append(UniquenessPlausability())

        return ret

    def get_stage_2_checks(self) -> list[Check]:
        ret = []

        for col in self.config_json["columns"]:
            if col["dtype"] == "int64" or col["dtype"] == "float64":
                ret.append(NumericValueConformanceCheck(col["name"], col["min"], col["max"]))

            elif col["dtype"] == "date":
                ret.append(
                    TemporalValueConformance(
                        col["name"],
                        col.get("min") if col.get("min") is not None else MIN_DATE,
                        col.get("max") if col.get("max") is not None else MAX_DATE,
                    )
                )

            elif col["dtype"] == "category":
                ret.append(StringValueConformance(col["name"], col["values"]))

            elif col["dtype"] == "bool":
                ret.append(StringValueConformance(col["name"], ["True", "False"]))

            elif col["dtype"] == "ordinal":
                ret.append(StringValueConformance(col["name"], col["values"]))

            else:
                raise RuntimeError(f"Unknown column type {col['type']} for column {col['name']}.")

        return ret

    def get_stage_3_checks(self) -> list[Check]:
        ret = []

        if "checks" in self.config_json:
            for check in self.config_json["checks"]:
                try:
                    f = self._json_to_check(check)
                    ret.append(f)
                except Exception as e:
                    raise RuntimeError(f"Error creating {check}: {e}")
        return ret

    def get_parsers(self) -> list[Parser]:

        ret = []

        if "parsers" in self.config_json:
            for parser in self.config_json["parsers"]:
                try:
                    f = self._json_to_parser(parser)
                    ret.append(f)
                except Exception as e:
                    raise RuntimeError(f"Error creating {parser}: {e}")
        return ret
