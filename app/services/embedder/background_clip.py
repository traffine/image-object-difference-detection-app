import io

import cv2
import numpy as np
import torch
import torchvision
from core.config import U2NET_PATH
from numpy import ndarray
from PIL import Image
from services.embedder.u2net import U2NET_full
from torch.autograd import Variable

u2net = U2NET_full()
u2net.load_state_dict(torch.load(U2NET_PATH, map_location="cpu"))
u2net.eval()


def norm_pred(d: torch.Tensor) -> torch.Tensor:
    """Regularize u2net output

    Returns a sensor that regularizes the output of u2net

    Args:
        d (torch.Tensor): tensor

    Returns:
        torch.Tensor: tensor
    """
    ma = torch.max(d)
    mi = torch.min(d)
    dn = (d - mi) / (ma - mi)
    return dn


def get_mask(image: Image.Image, predict: torch.Tensor) -> Image.Image:
    """Return u2net Inference Results

    Return u2net inference results

    Args:
        image (Image.Image): PIL data
        predict (torch.Tensor): u2net output

    Returns:
        Image.Image: PIL data
    """
    predict = predict.squeeze()
    predict_np = predict.cpu().data.numpy()
    im = Image.fromarray(predict_np * 255).convert("RGB")
    imo = im.resize((image.size[0], image.size[1]), resample=Image.Resampling.BILINEAR)
    return imo


def pil2cv(image: Image.Image) -> ndarray:
    """PIL -> OpenCV

    Returns images converted from PIL to OpenCV for image synthesis
    ref: https://qiita.com/derodero24/items/f22c22b22451609908ee

    Args:
        image (Image.Image): PIL data

    Returns:
        ndarray: numpy array (OpenCV)
    """
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # monochrome
        pass
    elif new_image.shape[2] == 3:  # color
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # transmission
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image


def clip_background(bytes_input: bytes) -> ndarray:
    """Crop the background of an image with u2net

    Return image with background cropped by u2net

    Args:
        bytes_input (bytes): bytes

    Returns:
        ndarray: numpy array
    """
    pil_input = Image.open(io.BytesIO(bytes_input))
    tensor_input = torchvision.transforms.functional.to_tensor(pil_input)
    tensor_input = Variable(tensor_input)
    tensor_input = tensor_input.unsqueeze(0)

    d1, _, _, _, _, _, _ = u2net(tensor_input)

    pred = d1[:, 0, :, :]
    pred = norm_pred(pred)

    mask = get_mask(pil_input, pred)
    image = pil2cv(pil_input)

    mask = cv2.bitwise_not(pil2cv(mask))

    blend = cv2.add(image, mask)

    return blend
