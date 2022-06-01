"""This API is used to calculate the salary of a person.
Furthermore there is a simple API to multiply the number by 2.

To update the API to google cloud:
gcloud app deploy app.yaml --project=tactile-petal-350412

Used environment: api_env
"""


from flask import Flask, request
from PIL import Image, ImageOps
import numpy as np

from ocr import ocr

app = Flask(__name__)

def convert_to_image(orig_image):
    """
    Depricated, no longer used.
    """
    img = Image.open(orig_image)  # load with Pillow
    print("Image size", img.size) # show image size (width, height)
    img = img.convert('RGB')       # convert to RGB, or Grayscale L
    print("RGB conversion")


def single_pic_proc(orig_image):
    """
    prediction for a single image
    :param image:
    :return: result texts and bboxes
    """
    img = Image.open(orig_image)  # load with Pillow
    img = img.convert('RGB')   # convert to 'RGB' or Grayscale 'L' 
    image = ImageOps.exif_transpose(img)
    image = np.array(image)
    result, image_framed = ocr(image)
    return result, image_framed

@app.route("/", methods=["GET"])
def instructions() -> str:
    """This function returns the instructions for the API.
    :return: A dictionary that contains the instructions"""
    return "Alive, please send a POST request to \
        predict with the following fields: \
        {'image' : '<image file>'}"

@app.route("/expiry", methods=["POST"])
def expiry_date() -> dict:
    """This function returns the expiry date of the image.
    :return: A dictionary that contains the expiry date."""
    image = request.files['image']
    filename = image.filename
    if filename.endswith('jpg') or filename.endswith('png'):
            convert_to_image(image)
            result, image_framed = single_pic_proc(image)
            result_list = []
            for key in result:
                result_list.append(result[key][1])
            return {"texts": result_list}
    return {"prediction": "No text found"}


@app.route("/predict", methods=["POST"])
def predict() -> dict:
    """
    This API tries to find the expiry date from a picture. 
    :return: dictionary that contains the expiry date of the picture.
    """
    image = request.files['image']
    content_json = request.get_json()
    keys = content_json.keys()
    if "image" in keys:
        return {"expiry_date": "2018-12-12"}
    else:
        return {"error": "no image in request"}

if __name__ == "__main__":
    app.run()

