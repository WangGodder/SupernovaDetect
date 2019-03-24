# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : Godder
# @Github  : https://github.com/WangGodder
from PIL import Image
from dataset.utils import read_csv
import time
import os


def open_image_with_target(targets, file_dir="F:/datasets/af2019-cv-training-20190312-show", list_dir="F:/datasets/af2019-cv-training-20190312"):
    """
    open image with input target
    :param targets: the target want to show
    :param file_dir: the dir of image
    :param list_dir: the dir of list.csv
    :return:
    """
    csv = read_csv(os.path.join(list_dir, 'list.csv'))  # type:dict
    for id, labels in csv.items():
        if labels[2] in targets:
            img = Image.open(os.path.join(file_dir, str(id[0:2]), id + '_b.jpg'))   # type: Image
            time.sleep(1)
            img.show()


if __name__ == '__main__':
    open_image_with_target(['isstar'])