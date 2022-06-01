import os
from ocr import ocr
import time
import shutil
import numpy as np
from PIL import Image
from glob import glob
import cv2
import re
from text_date_extraction import extract_date

def single_pic_proc(image_file):
    image = np.array(Image.open(image_file).convert('RGB'))
    result, image_framed = ocr(image)
    return result,image_framed

def dis(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys
    if len(sys.argv)>=2:
        filename = sys.argv[1]
        if filename.endswith('jpg') or filename.endswith('png'):
            result, image_framed = single_pic_proc(filename)

            txt_out = ""
            for key in result:
                txt_out += f" {result[key][1]}"
            print(txt_out)

            if txt_out == "":
                print("The model could not detect anything.")
            else:
                exp_date = extract_date(txt_out)
                print(exp_date)