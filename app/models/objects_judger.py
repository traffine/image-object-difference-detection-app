from enum import Enum
from typing import List, Union

from pydantic import BaseModel


class Similarity(BaseModel):
    rank: int
    id_b: Union[str, None]
    similarity: float


class Result(BaseModel):
    id_a: str
    id_b_matched: Union[str, None]
    id_b_switched: Union[str, None]
    is_disappeared: Union[bool, None]
    similarities: List[Similarity]


class DiffType(str, Enum):
    SWITCHED = "SWITCHED"
    DISAPPEARED = "DISAPPEARED"
    ADDITIONAL = "ADDITIONAL"


class Judgement(BaseModel):
    has_diff: bool
    diff_types: List[DiffType]
    results: List[Result]
