import io
from typing import Union

import numpy as np
from fastapi.datastructures import UploadFile
from fastapi.param_functions import File
from fastapi.responses import Response
from fastapi.routing import APIRouter
from loguru import logger
from models.objects_embedder import EmbeddedObjects
from PIL import Image
from services.embedder.objects_embedder import ObjectsEmbedder

router = APIRouter()


@router.post(
    "/embed",
    response_model=EmbeddedObjects,
    name="Extract feature vectors of each object from JPG images",
)
async def embed_objects(
    image: UploadFile = File(...),
) -> Union[EmbeddedObjects, Response]:
    """Extract feature vectors of each object from JPG images

    Perform the following from input images
    1. object detection by Google Vision API
    2. background cropping by U2Net
    3. extract the background cropped object image from the background cropped image using the bbox of each object obtained by Google Vision API
    4. feature vector extraction by EfficientNet

    Args: image (UploadFile): JPG image

    Returns:
        Union[EmbeddedObjects, Response]: embedded objects
    """
    if image.content_type not in ["image/jpg", "image/jpeg"]:
        logger.error("input format is wrong")
        return Response(status_code=400)

    try:
        image_ndarray = np.array(Image.open(io.BytesIO(image.file.read())))

        object_embedder = ObjectsEmbedder()
        return object_embedder.process(image=image_ndarray)
    except Exception as e:
        logger.error(e)
        return Response(status_code=500)
