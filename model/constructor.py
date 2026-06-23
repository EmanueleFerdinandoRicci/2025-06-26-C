from dataclasses import dataclass


@dataclass
class Constructor:
    constructorId:int
    constructorRef:str
    name:str
    nationality:str
    url:str
    results:dict

    def __hash__(self):
        return hash(self.constructorId)

    def __str__(self):
        return f"{self.constructorRef} ({self.name})"

