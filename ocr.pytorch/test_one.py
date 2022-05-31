import os
from ocr import ocr
import time
import shutil
import numpy as np
from PIL import Image, ImageOps
from glob import glob
import cv2

def single_pic_proc(image_file):
    image = Image.open(image_file).convert('RGB')
    image = ImageOps.exif_transpose(image)
    image = np.array(image)
    result, image_framed = ocr(image)
    return result, image_framed

def dis(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        if filename.endswith('jpg') or filename.endswith('png'):
            result, image_framed = single_pic_proc(filename)
            print(result)
            for key in result:
                print(result[key][1])
            #dis(image_framed)
