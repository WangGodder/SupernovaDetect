# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : Godder
# @Github  : https://github.com/WangGodder
import torch
import torch.nn.functional as F
import torch.nn as nn


class Deep_HiTS(nn.Module):
    """
    根据论文Enhanced Rotational Invariant Convolutional Neural Network for Supernovae Detection 创建的Deep_HiTS模型
    输入为旋转好的4组图像
    """
    def __init__(self):
        super(Deep_HiTS, self).__init__()
        self.conv1 = nn.Conv2d(4 * 4, 32, 4, 1, padding=3, dilation=1, groups=1, bias=True)    # input(21,21)output(24, 24)
        self.conv2 = nn.Conv2d(32, 32, 3, 1, padding=1, dilation=1, groups=1, bias=True)
        self.maxpool1 = nn.MaxPool2d(2, stride=2, padding=0, dilation=1, return_indices=False, ceil_mode=False)
        self.conv3 = nn.Conv2d(32, 64, 3, 1, padding=1, dilation=1, groups=1, bias=True)    # input(12, 12)output(12,12)
        self.conv4 = nn.Conv2d(64, 64, 3, stride=1, padding=1, dilation=1, groups=1, bias=True)
        self.conv5 = nn.Conv2d(64, 64, 3, stride=1, padding=1, dilation=1, groups=1, bias=True)
        self.maxpool2 = nn.MaxPool2d(2, stride=2, padding=0, dilation=1, return_indices=False, ceil_mode=False)
        self.dense1 = nn.Linear(6 * 6 * 64 * 4, 64, bias=True)
        self.dense2 = nn.Linear(64, 64, bias=True)
        self.dense3 = nn.Linear(64, 2, bias=True)
        self.out = nn.Softmax(dim=1)

    def forward(self, input):
        x = self.conv1(input)
        x = self.conv2(x)
        x = self.maxpool1(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.conv5(x)
        x = self.maxpool2(x)
        x = x.view(x.size(0), -1)
        x = self.dense1(x)
        x = self.dense2(x)
        x = self.dense3(x)
        out = self.out(x)
        return out


def create():
    return Deep_HiTS()

