from dataclasses import dataclass
from typing import List, Union

import numpy as np
from core.config import SIMILARITY_THRESHOLD
from models.objects_embedder import EmbeddedObjects
from models.objects_judger import DiffType, Judgement


@dataclass
class ObjectsJudger:
    """Object Judgement"""

    objects_a: EmbeddedObjects
    objects_b: EmbeddedObjects

    def cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate Cosine similarity of feature vectors

        Return the cosine similarity from feature vectors

        Args:
            a (List[float]): embedding of a
            b (List[float]): embedding of b

        Returns:
            float: cosine similarity
        """
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def process(self, threshold: float = SIMILARITY_THRESHOLD) -> Judgement:
        """Return similarity judgment of an object

        Return the result of object determination

        Args:
            threshold (float): Similarity threshold

        Returns:
            Judgement
        """
        results = []
        for obj_a in self.objects_a:
            similarities = []
            for obj_b in self.objects_b:
                similarities.append(
                    {
                        "id_b": obj_b.id,
                        "similarity": self.cosine_similarity(obj_a.embedding.embedding, obj_b.embedding.embedding),
                    }
                )
            similarities = sorted(similarities, key=lambda x: x["similarity"], reverse=True)
            for i in range(len(similarities)):
                similarities[i]["rank"] = i + 1

            results.append({"id_a": obj_a.id, "similarities": similarities})

        diff_types: List[DiffType] = []

        len_a = len(self.objects_a)
        len_b = len(self.objects_b)
        len_diff = len_a - len_b

        if len_diff < 0:
            diff_types.append(DiffType.ADDITIONAL)

        for result in results:
            id_b_matched = None

            i = 0
            while i < len_b:
                similarity = result["similarities"][i]["similarity"]
                if similarity > threshold:
                    id_b = result["similarities"][i]["id_b"]
                    similarities_id_b = [list(filter(lambda x: x["id_b"] == id_b, r["similarities"]))[0]["similarity"] for r in results]
                    if similarity == max(similarities_id_b):
                        id_b_matched = id_b
                        break
                i = i + 1

            result["id_b_matched"] = id_b_matched

        ids_b_matched = [result["id_b_matched"] for result in results if isinstance(result["id_b_matched"], str)]

        num_unmatched = max(len_a, len_b) - len(ids_b_matched)

        for result in results:
            id_b_switched = None
            is_disappeared: Union[bool, None] = False

            if result["id_b_matched"] is None:
                if len_diff == 0:
                    diff_types.append(DiffType.SWITCHED)
                    if num_unmatched == 1:
                        id_b_switched = list(set([t.id for t in self.objects_b]) - set(ids_b_matched))[0]
                    else:
                        id_b_switched = "unknown"
                elif len_diff > 0:
                    diff_types.append(DiffType.DISAPPEARED)
                    if abs(len_diff) == num_unmatched:
                        is_disappeared = True
                    else:
                        is_disappeared = None
                        id_b_switched = "unknown"
                        diff_types.append(DiffType.SWITCHED)
                elif len_diff < 0:
                    if abs(len_diff) != num_unmatched:
                        id_b_switched = "unknown"
                        diff_types.append(DiffType.SWITCHED)

            result["id_b_switched"] = id_b_switched
            result["is_disappeared"] = is_disappeared

        diff_types = list(set(diff_types))

        return Judgement(has_diff=False if len(diff_types) == 0 else True, diff_types=diff_types, results=results)
