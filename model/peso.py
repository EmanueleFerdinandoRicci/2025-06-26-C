from dataclasses import dataclass

from model.constructor import Constructor


@dataclass
class Peso:
    c: Constructor
    numeroGare: int