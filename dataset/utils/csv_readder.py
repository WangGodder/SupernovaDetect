# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : Godder
# @Github  : https://github.com/WangGodder

import csv


def read_csv(csv_file):
    """
    读取比赛官方的list.csv文件，并返回dict对象
    :param csv_file: list.csv的路径
    :return: dict{id : [x, y , type]}
    """
    reader = csv.reader(open(csv_file, 'r'))
    next(reader)
    result = {}
    for line in reader:
        id, x, y, type = line
        result[id] = [x, y, type]
    return result

