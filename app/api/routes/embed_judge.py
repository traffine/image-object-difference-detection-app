import io
from typing import Union

import numpy as np
from core.config import SIMILARITY_THRESHOLD
from fastapi.datastructures import UploadFile
from fastapi.param_functions import File
from fastapi.responses import Response
from fastapi.routing import APIRouter
from loguru import logger
from models.objects_judger import Judgement
from PIL import Image
from services.embedder.objects_embedder import ObjectsEmbedder
from services.judger.objects_judger import ObjectsJudger

router = APIRouter()


@router.post(
    "/embed-and-judge",
    response_model=Judgement,
    name="EMBED and JUDGE in succession.",
)
async def embed_objects(
    image_a: UploadFile = File(...),
    image_b: UploadFile = File(...),
) -> Union[Judgement, Response]:
    """EMBED and JUDGE in succession.

    Args:
        image_a (UploadFile): JPG image a
        image_b (UploadFile): JPG image b

    Returns:
        Union[Judgement, Response]: judgement results
    """
    for image in [image_a, image_b]:
        if image.content_type not in ["image/jpg", "image/jpeg"]:
            logger.error("input format is wrong")
            return Response(status_code=400)

    try:
        image_a_ndarray = np.array(Image.open(io.BytesIO(image_a.file.read())))
        image_b_ndarray = np.array(Image.open(io.BytesIO(image_b.file.read())))

        object_embedder = ObjectsEmbedder()
        objects_a = object_embedder.process(image=image_a_ndarray)
        objects_b = object_embedder.process(image=image_b_ndarray)

        objects_judger = ObjectsJudger(objects_a=objects_a.objects, objects_b=objects_b.objects)
        return objects_judger.process(threshold=SIMILARITY_THRESHOLD)
    except Exception as e:
        logger.error(e)
        return Response(status_code=500)
