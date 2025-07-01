# Parse the config of the files
# Author: Bruno Scharlau, 28.06.2025
import os
import json

from src.checks.check import Check

from src.checks.computational.check_bmi import BMICheck

from src.checks.conformance.numeric_value_conformance import NumericValueConformanceCheck
from src.checks.conformance.string_value_conformance import StringValueConformance
from src.checks.conformance.temporal_value_conformance import TemporalValueConformance

from src.checks.plausability.temporal_order_plausability import TemporalOrderPlausability

from src.parsers.parser import Parser


class Config():

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
        return Parser(
            mapping=json["mapping"],
            columns=json["columns"],
            case_sensitive=json.get("case_sensitive", False)
        )

    def _json_to_check(self, json):
        if "check_type" not in json.keys():
            raise KeyError("check_type not defined.")

        check_type = json["check_type"]

        if check_type == "temporal_value_conformance":
            return TemporalValueConformance(
                json["column"],
                json["date_range"]["start"],
                json["date_range"]["end"],
                json.get("inclusive", False),
                json.get("allow_na", False)
            )
        
        elif check_type == "string_value_conformance":
            return StringValueConformance(
                json["column"],
                json["values"],
                json.get("allow_na", False)
            )
        
        elif check_type == "temporal_order_plausability":

            return TemporalOrderPlausability(
                json["first"],
                json["last"],
                json.get("inclusive", False),
                json.get("allow_na", False)
            )
        
        raise RuntimeError(f"Check for type {check_type} not configured.")


    def get_checks(self) -> list[Check]:

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
    
