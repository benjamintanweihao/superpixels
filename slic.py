import urllib
import numpy as np
import cv2

from urllib.request import urlopen, Request
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float


def download_image(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as url:
        resp = url.read()
        image = np.asarray(bytearray(resp), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        return image


def get_superpixel_masks_and_boundaries(image, n_segments=100):
    # TODO: take color in as parameter
    color = (0, 255, 0)

    image = img_as_float(image)
    segments = slic(image, n_segments=n_segments, sigma=5)

    # make empty image to layer boundaries
    empty = np.zeros(image.shape[:2], dtype=np.uint8)
    boundaries = mark_boundaries(empty, segments, color=color, outline_color=color)

    # make background transparent
    boundaries = cv2.cvtColor(np.array(boundaries, dtype=np.uint8), cv2.COLOR_BGR2RGBA)
    boundaries[np.where((boundaries == [0, 0, 0, 255]).all(axis=2))] = [0, 0, 0, 0]

    masks = []

    # convert image to have an alpha channel
    image = cv2.cvtColor(np.array(image, dtype=np.uint8), cv2.COLOR_RGB2RGBA)
    for (i, segval) in enumerate(np.unique(segments)):
        image[segments == segval] = (255, 0, 0, 127)
        image[segments != segval] = (0, 0, 0, 0)

        masks.append(image)

    return masks, boundaries
