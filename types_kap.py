from dataclasses import dataclass


@dataclass
class ResponseVCNum:
    min: float
    max: float
    above: int
    below: int
    missing: int
    total: int
    bad_id_list: list[int]


@dataclass
class ResponseVCStr:
    outside: int
    missing: int
    total: int
    bad_id_list: list[int]


@dataclass
class ResponseVCDate:
    before: int
    after: int
    missing: int
    total: int
    bad_id_list: list[int]


@dataclass
class ResponseVCDateOrder:
    earlier: int
    missing: int
    total: int
    bad_id_list: list[int]
