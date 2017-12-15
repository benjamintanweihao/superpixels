from functools import wraps
from slic import download_image, get_superpixel_masks_and_boundaries
from flask import Flask, request, jsonify, current_app
from urllib.parse import unquote

import cv2
import base64


app = Flask(__name__)


def jsonp(func):
    """Wraps JSONified output for JSONP requests."""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data, "utf-8")
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)

    return decorated_function


@app.route("/api/superpixel", methods=['GET'])
@jsonp
def segment():
    url = unquote(request.args.get('url'))
    n_segs = int(request.args.get('n_segs', 100))

    if n_segs < 100: n_segs = 100
    if n_segs > 500: n_segs = 500

    if url is not None:
        image = download_image(url)
        masks, boundaries = get_superpixel_masks_and_boundaries(image, n_segs)

        masks_as_text = []

        for m in masks:
            _, buffer = cv2.imencode('.png', m)
            mask_as_text = str(base64.b64encode(buffer), 'utf-8')
            masks_as_text.append(mask_as_text)
            print(mask_as_text)


        _, buffer = cv2.imencode('.png', boundaries)
        boundaries_as_text = str(base64.b64encode(buffer), 'utf-8')

        return jsonify({"masks": masks_as_text, "boundaries": boundaries_as_text})