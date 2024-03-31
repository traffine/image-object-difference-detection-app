from typing import Union

from core.config import SIMILARITY_THRESHOLD
from fastapi.responses import Response
from fastapi.routing import APIRouter
from loguru import logger
from models.objects_embedder import EmbeddedObjects
from models.objects_judger import Judgement
from services.judger.objects_judger import ObjectsJudger

router = APIRouter()


@router.post(
    "/judge",
    response_model=Judgement,
    name="Differential judgment of objects",
)
async def judge_objects(
    objects_a: EmbeddedObjects,
    objects_b: EmbeddedObjects,
) -> Union[Judgement, Response]:
    """Differential judgment of objects

    Cosine similarity comparison of each object in image a and image b to determine the similarity for each object in image a.

    Args:
        objects_a (EmbeddedObjects): image a with embedded
        objects_b (EmbeddedObjects): image b with embedded API

    Returns:
        Union[Judgement, Response]: Judgement results
    """
    try:
        objects_judger = ObjectsJudger(objects_a=objects_a.objects, objects_b=objects_b.objects)
        return objects_judger.process(threshold=SIMILARITY_THRESHOLD)

    except Exception as e:
        logger.error(e)
        return Response(status_code=500)
