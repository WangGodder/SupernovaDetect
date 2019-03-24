# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : Godder
# @Github  : https://github.com/WangGodder
from PIL import Image, ImageDraw
import numpy as np
import os


def get_mean_px(img):
    """
    calculate the mean pixel of image.
    :param img: the image to calculate
    :return: the value of the mean of input image
    """
    if type(img) == np.ndarray:
        return img.mean()
    else:
        return np.array(img, 'f').mean()


def sub_mean_img(img):
    img_array = img
    if type(img) != np.ndarray:
        img_array = np.array(img, 'f')
    img_array = np.subtract(img_array, int(get_mean_px(img_array)))
    print(img_array)
    return img_array


def get_radius(img, *center):
    # sub_mean = sub_mean_img(img)
    img = np.array(img)
    # print(sub_mean.shape)
    # print(sub_mean[center[1]][center[0]])
    radius = 1
    is_break = True
    while True:
        for col in range(center[0] - radius, center[0] + radius):
            for row in range(center[1] - radius, center[1] + radius):
                if img[row][col] > 255*0.8:
                    is_break = False
                    break
        if is_break:
            break
        radius += 1
    return radius


def mean_radius(target, img_dir):
    radius = list()

    return sum(radius)/len(radius)


if __name__ == '__main__':
    folder_url = "F:/datasets/af2019-cv-training-20190312/76/"
    img_url = os.path.join(folder_url, '76f141aad7ca74200f47c405991d1eb0_b.jpg')
    img = Image.open(img_url).convert('L')  # type: Image
    draw = ImageDraw.Draw(img)
    center = (81, 360)
    # draw.rectangle((center[0] - 4, center[1] - 4, center[0] + 4, center[1] + 4), None, 'red')
    # img.show()
    # crop_img = img.crop((center[0] - 4, center[1] - 4, center[0] + 4, center[1] + 4))
    # print(np.array(crop_img))
    # crop_img.show()
    radius = get_radius(img, center[0], center[1])
    # crop_img = img.crop((94 - 1, 94 + 1, 248 - 1, 248 + 1))
    # crop_img.show()

