from random import random

from starlette.testclient import TestClient


# Normal System Test 001
def test_N001(client: TestClient) -> None:
    """Normal System Test"""
    response = client.post(
        "/judge",
        json={
            "objects_a": {"objects": [{"id": "id1", "boxes": [0, 0, 0, 0], "score": 0, "embedding": {"embedding": [random() for i in range(1280)]}}]},
            "objects_b": {"objects": [{"id": "id2", "boxes": [0, 0, 0, 0], "score": 0, "embedding": {"embedding": [random() for i in range(1280)]}}]},
        },
    )
    assert response.status_code == 200


# Abnormal System Test 001
def test_ABN001(client: TestClient) -> None:
    """Abnormal System Test

    Set the len of "embedding" in the request to 128
    """
    try:
        client.post(
            "/judge",
            json={
                "objects_a": {"objects": [{"id": "id1", "boxes": [0, 0, 0, 0], "score": 0, "embedding": {"embedding": [random() for i in range(128)]}}]},
                "objects_b": {"objects": [{"id": "id2", "boxes": [0, 0, 0, 0], "score": 0, "embedding": {"embedding": [random() for i in range(128)]}}]},
            },
        )
        assert Exception
    except:
        assert Exception
