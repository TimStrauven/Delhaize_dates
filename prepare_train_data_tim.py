import os
import json
import cv2

base_path = "/home/tim/Desktop/ocr.pytorch/Korean dataset dates/Products-Real/evaluation/"
images_path = f"{base_path}images/"
cropped_img_path = f"{base_path}cropped_images/"
annotation_file = f"{base_path}annotations.json"
infofile = f"{base_path}infofile.txt"


"""create infofile and folder if it doesn't exist"""
if not os.path.exists(cropped_img_path):
    os.makedirs(cropped_img_path)
if os.path.exists(infofile):
    os.remove(infofile)
if not os.path.exists(infofile):
    with open(infofile, "w") as f:
        f.write("")

"loop trough the jpeg files in the image folder by reading trough the annotation file"
with open(annotation_file, "r") as f:
    images = json.load(f)


def save_cropped_image(image_path, bbox, save_path):
    """save the cropped image"""
    img = cv2.imread(image_path)
    xpd = 5
    cropped_image = img[(bbox[1] - xpd):(bbox[3] + xpd), (bbox[0] - xpd)
                         :(bbox[2] + xpd)]  # Slicing to crop the image
    cv2.imwrite(save_path, cropped_image)


for image in images:
    ann = images[image]["ann"]
    for i, ann_item in enumerate(ann):
        if "transcription" in images[image]["ann"][i]:
            bbox = images[image]["ann"][i]["bbox"]
            transcription = images[image]["ann"][i]["transcription"]
            print(f"img {image} has date {transcription} inside box {bbox}")
            save_img = image.replace(".jpg", "")
            save_img = f"{save_img}_{i}.jpg"
            save_cropped_image(f"{images_path}{image}",
                               bbox, f"{cropped_img_path}{save_img}")
            with open(infofile, "a") as f:
                split = r"\t"
                f.write(f"{cropped_img_path}{save_img}{split}{transcription}\n")
