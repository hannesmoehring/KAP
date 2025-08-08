from dataclasses import asdict, dataclass

MIN_DATE = "01.01.1900"
MAX_DATE = "01.04.2025"


@dataclass
class GenericResponse:
    type: str
    col: list[str]
    wrong: int
    missing: int
    total: int
    bad_id_list: list[int]
    failed: bool = False

    def to_dict(self):
        return asdict(self)


@dataclass
class Result:
    results_stage_1: list[GenericResponse]
    results_stage_2: list[GenericResponse]
    results_stage_3: list[GenericResponse]
    count_failed_stage_1: int
    count_failed_stage_2: int
    count_failed_stage_3: int
    bad_id_set: set[int]
