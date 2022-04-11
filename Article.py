import json
from dataclasses import dataclass

@dataclass
class Article:
    title: str
    url: str
    date: str
    publisher: str
    citation_count: int
    reference_count: int
    references: list
    citations: list

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
