# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : Godder
# @Github  : https://github.com/WangGodder
import numpy as np


def snr_variance(img):
    avg = img.mean()    # 获取图像的总体均值
    std = np.std(img, ddof=1)
    return avg/std


def snr_filter(img, img_filter):
    return np.divide(img_filter, img)
