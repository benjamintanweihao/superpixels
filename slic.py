import base64
import urllib
import numpy as np
import cv2

from urllib.request import urlopen, Request
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io
import matplotlib.pyplot as plt

url = "https://i.imgur.com/Q7xoeiA.png"


# url = "https://i.imgur.com/68XbDC7.jpg"

def download_image(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as url:
        resp = url.read()
        image = np.asarray(bytearray(resp), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        return image


def get_superpixel_masks(image, n_segments=100):
    image = img_as_float(image)

    segments = slic(image, n_segments=n_segments, sigma=5)

    # cv2.imshow('', mark_boundaries(image, segments))
    # cv2.waitKey(0)

    masks = []

    # convert image to have an alpha channel
    image = cv2.cvtColor(np.array(image, dtype=np.uint8), cv2.COLOR_RGB2RGBA)
    for (i, segval) in enumerate(np.unique(segments)):
        image[segments == segval] = (255, 0, 0, 127)
        image[segments != segval] = (0, 0, 0, 0)

        masks.append(image)
        # cv2.imwrite(str(segval) + '.png', image)

    return segments
