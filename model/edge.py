from dataclasses import dataclass

from model.constructor import Constructor


@dataclass
class Edge:
    constructor1: Constructor
    constructor2: Constructor
    peso: int