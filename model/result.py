from dataclasses import dataclass


@dataclass
class Result:
    cId: int
    year: int
    rId: int
    dId: int
    position: int