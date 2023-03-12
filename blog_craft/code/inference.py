import os
from six import BytesIO
import cv2
import numpy as np
import json

from craft import *


def model_fn(model_dir):
    return CRAFT.load_from_pretrained(os.path.join(model_dir, "craft.pth"))


def input_fn(request_body, request_content_type):
    # binary
    rawdata = BytesIO(request_body).read()
    
    # deserialize
    image:np.ndarray = cv2.imdecode(np.frombuffer(rawdata, np.uint8), flags=cv2.IMREAD_COLOR)
    
    return image, 0.01, 30, 0.3


def predict_fn(input_data, model):
    return model(*input_data)


def output_fn(prediction, content_type):
    response = json.dumps(prediction, sort_keys=False)
    
    return response, "application/json"
