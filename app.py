"""This API is used to calculate the salary of a person.
Furthermore there is a simple API to multiply the number by 2.

To update the API to google cloud:
gcloud app deploy app.yaml --project=tactile-petal-350412

Used environment: api_env
"""

import os
from flask import Flask, request
from PIL import Image, ImageOps
import numpy as np
from ocr import ocr
from text_date_extraction import extract_date

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
    return "API is alive, please send a image as a POST request \
        to the /expiry endpoint."

@app.route("/expiry", methods=["POST"])
def expiry_date() -> dict:
    """This function returns the expiry date of the image.
    :return: A dictionary that contains the expiry date."""
    image = request.files['image']
    filename = image.filename
    if filename.endswith('jpg') or filename.endswith('png'):
            #convert_to_image(image)
            result, image_framed = single_pic_proc(image)
            #result_list = []
            #for key in result:
            #    result_list.append(result[key][1])
            #return {"texts": result_list}
    #return {"prediction": "No text found"}
            txt_out = ""
            for key in result:
                txt_out += f" {result[key][1]}"
            print(txt_out)

            if txt_out == "":
                return {"prediction": "The model could not detect anything."}
            else:
                exp_date = extract_date(txt_out)
                return {"prediction": exp_date}

if __name__ == '__main__':
    # You want to put the value of the env variable PORT if it exist (some services only open specifiques ports)
    port = int(os.environ.get('PORT', 5000))
    # Threaded option to enable multiple instances for
    # multiple user access support
    # You will also define the host to "0.0.0.0" because localhost will only be reachable from inside de server.
    app.run(host="0.0.0.0", threaded=True, port=port)
