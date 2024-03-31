from typing import Any, List

from pydantic import BaseModel, Field


class Embedding(BaseModel):
    embedding: List[float] = Field(..., min_length=1280, max_length=1280)


class GVisionObject(BaseModel):
    id: str
    boxes: List[float] = Field(..., min_length=4, max_length=4)
    score: float


class EmbeddedObject(GVisionObject):
    image: Any
    embedding: Embedding


class EmbeddedObjects(BaseModel):
    objects: List[EmbeddedObject]
