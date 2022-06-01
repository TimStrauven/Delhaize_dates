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
from text_date_extraction import extract_date
from recognize.crnn_recognizer import PytorchOcr
recognizer = PytorchOcr()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def instructions() -> str:
    """This function returns the instructions for the API.
    :return: A dictionary that contains the instructions"""
    return "API is alive, please send a image as a POST request \
        to the /expiry endpoint."

@app.route("/cropped", methods=["POST"])
def cropped_date() -> str:
    """This function returns the expiry date of the image.
    :return: A dictionary that contains the expiry date."""
    image = request.files['image']
    filename = image.filename
    if filename.endswith('jpg') or filename.endswith('png'):
        image = Image.open(image).convert('RGB')
        image = ImageOps.exif_transpose(image)
        image = np.array(image)
        date = recognizer.recognize(image)
        return date

if __name__ == "__main__":
    app.run(debug=True)
