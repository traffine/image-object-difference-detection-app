import os

VERSION = "0.1.0"
DEBUG = os.environ.get("DEBUG", False)
PROJECT_NAME = os.environ.get("PROJECT_NAME", "object-diff")

# Cosine similarity threshold
SIMILARITY_THRESHOLD: float = 0.6

# Image resizing RESOLUTION
IMAGE_RESOLUTION_WIDTH: int = 480
IMAGE_RESOLUTION_HEIGHT: int = 480

# Model path
EFFNET_PATH = "./efficientnet_v2_imagenet21k_l_feature_vector_2.onnx"
U2NET_PATH = "./u2net.pth"
