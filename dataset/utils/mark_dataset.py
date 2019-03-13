# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : Godder
# @Github  : https://github.com/WangGodder

import cv2 as cv
import os
from csv_readder import read_csv

def mark_image(image_url, x, y, color=(0, 0, 255), radius=10):
    """
    标记指定图像
    :param image_url: 图像路径
    :param x: 圆心x坐标
    :param y: 圆心y坐标
    :param color: 颜色
    :param radius: 半径
    :return: 返回标记后的图像
    """
    img = cv.imread(image_url)
    cv.circle(img, (x, y), radius, color)
    return img


def save_image(img, save_url):
    """
    保存图像
    :param img: cv生成的图像对象
    :param save_url: 存放路径
    :return:
    """
    cv.imwrite(save_url, img)


def mark_all_database(folder_url, output_url):
    """
    将所有数据图像按照list.csv标记，星体为红色，其他为绿色
    :param folder_url: 数据文件根目录
    :param output_url: 导出数据根目录
    :return:
    """
    csv = read_csv(os.path.join(folder_url, 'list.csv'))    #type:dict
    index = 0
    for id, labels in csv.items():
        index += 1
        dir_path = os.path.join(folder_url, str(id)[0:2])
        file_path = os.path.join(dir_path, id + '_c.jpg')
        print("current image :", file_path, index, "/" ,csv.__len__())
        if (labels[2] in ['newtarget', 'isstar', 'asteroid', 'isnova', 'known']):
            img = mark_image(file_path, int(labels[0]), int(labels[1]))
        else:
            img = mark_image(file_path, int(labels[0]), int(labels[1]), color=(0, 255, 0))
        if not os.path.exists(os.path.join(output_url, str(id)[0:2])):
            os.mkdir(os.path.join(output_url, str(id)[0:2]))
        save_image(img, os.path.join(output_url, str(id)[0:2], id + '_c.jpg'))
        print("write to ", os.path.join(output_url, str(id)[0:2], id + '_c.jpg'))
    return



if __name__ == '__main__':
    folder_url = "F:/datasets/af2019-cv-training-20190312"
    output_url = "F:/datasets/af2019-cv-training-20190312-show"
    mark_all_database(folder_url, output_url)
