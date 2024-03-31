import io
import uuid
from typing import List

import numpy as np
import onnxruntime
from core.config import EFFNET_PATH, IMAGE_RESOLUTION_HEIGHT, IMAGE_RESOLUTION_WIDTH
from google.cloud import vision_v1
from models.objects_embedder import EmbeddedObject, EmbeddedObjects, Embedding, GVisionObject
from numpy import ndarray
from PIL import Image
from services.embedder.background_clip import clip_background

onnx_session = onnxruntime.InferenceSession(EFFNET_PATH)
input_name = onnx_session.get_inputs()[0].name
output_name = onnx_session.get_outputs()[0].name


class ObjectsEmbedder:
    def resize_image(self, image: ndarray) -> bytes:
        """Resize an image and return it in Bytes

        Resize an image and return it in Bytes

        Args:
            image (ndarray): input image

        Returns:
            bytes: resized image
        """
        pil_input = Image.fromarray(image).resize((512, 512), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        pil_input.save(buf, format="JPEG")
        return buf.getvalue()

    def detect_objects(self, bytes_input: bytes) -> List[GVisionObject]:
        """Detect objects from byte images

        Perform object detection with Google Vision API and return a list of bboxes, scores, and cropped images for each object.

        Args:
            bytes_input (bytes): bytes image

        Returns:
            list[GVisionObject]
        """
        client = vision_v1.ImageAnnotatorClient()
        response = client.object_localization(image=vision_v1.Image(content=bytes_input)).localized_object_annotations

        objects = []
        for obj in response:
            start = obj.bounding_poly.normalized_vertices[0]
            end = obj.bounding_poly.normalized_vertices[2]
            objects.append(GVisionObject(id=f"{obj.name}_{str(uuid.uuid4())}", boxes=[start.x, start.y, end.x, end.y], score=obj.score))

        return objects

    @staticmethod
    def embed(image: ndarray) -> Embedding:
        """Embed by Efficientnet

        Return feature vectors from ndarray image data by Efficientnet

        Args:
            image (ndarray): ndarray

        Returns:
            Embedding: List[float] of length 1280
        """
        image_pil = Image.fromarray(image)
        image_pil = image_pil.convert("RGB")
        image_pil = image_pil.resize((IMAGE_RESOLUTION_WIDTH, IMAGE_RESOLUTION_HEIGHT))
        image_pil = np.array(image_pil, dtype=np.float32)
        image_pil = image_pil / 255

        embedding = onnx_session.run([output_name], {input_name: np.expand_dims(image_pil, 0)})[0][0].tolist()

        return Embedding(embedding=embedding)

    def process(self, image: ndarray) -> EmbeddedObjects:
        """Process

        Args:
            image (ndarray): input image

        Returns:
            EmbeddedObjects
        """
        image_resized = self.resize_image(image=image)

        objects_detected = self.detect_objects(bytes_input=image_resized)
        image_clipped: ndarray = clip_background(bytes_input=image_resized)

        h, w, _ = image_clipped.shape

        objects = []
        for obj in objects_detected:
            box_half_height = int(((obj.boxes[3] - obj.boxes[1]) * h / 2) + 0.5)
            box_half_width = int(((obj.boxes[2] - obj.boxes[0]) * w / 2) + 0.5)
            x_center = int(sum([obj.boxes[0] * w, obj.boxes[2] * w]) / 2)
            y_center = int(sum([obj.boxes[1] * h, obj.boxes[3] * h]) / 2)

            output_image = image_clipped[
                y_center - box_half_height : y_center + box_half_height,
                x_center - box_half_width : x_center + box_half_width,
                :,
            ]
            embedding = self.embed(image=output_image)
            objects.append(
                EmbeddedObject(
                    id=obj.id,
                    boxes=obj.boxes,
                    score=obj.score,
                    image=output_image,
                    embedding=Embedding(embedding=embedding.embedding),
                )
            )

        return EmbeddedObjects(objects=objects)
