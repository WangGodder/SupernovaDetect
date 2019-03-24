# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : Godder
# @Github  : https://github.com/WangGodder
import cv2
from PIL import Image
import numpy as np
from dataset.utils import *
import os


def normalize_img(img):
    out = np.zeros(img.shape)
    cv2.normalize(img, out, norm_type=cv2.NORM_L1)
    return out


if __name__ == '__main__':
    folder_url = "F:/datasets/af2019-cv-training-20190312/00/"
    img_url = os.path.join(folder_url, '000db175d712996f1cfd20cc7d600223_a.jpg')
    img = Image.open(img_url).convert('L')   # type: Image
    img.show()
    out = normalize_img(np.array(img, 'f'))
    print(out)
    # out = normalize_img(img)
    # cv2.imshow(out)


