# -*- coding: utf-8 -*-
# @Time    : 2019/3/27
# @Author  : Godder
# @Github  : https://github.com/WangGodder
import torch
import torch.nn as nn
import torch.nn.functional as F
from .layer import PriorBoxLayer


class ConvBN(nn.Module):
    """
    the conv layer with batch norm
    """
    def __init__(self, in_channels, out_channels, kernel_size=1, stride=1, padding=0, relu=False):
        super(ConvBN, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride, padding=padding)
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = relu

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        if self.relu:
            x = F.relu(x, inplace=True)
        return x


class Bottleneck(nn.Module):
    """
    the bottle neck layers model
    contains 3 conv with batch norm and down sample if needed
    """
    expansion = 4

    def __init__(self, in_planes, planes, stride=1):
        super(Bottleneck, self).__init__()
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, self.expansion*planes, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(self.expansion*planes)

        self.downsample = nn.Sequential()
        if stride != 1 or in_planes != self.expansion*planes:
            self.downsample = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion*planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)),inplace=True)
        out = F.relu(self.bn2(self.conv2(out)),inplace=True)
        out = self.bn3(self.conv3(out))
        out += self.downsample(x)
        out = F.relu(out,inplace=True)
        return out


class Context_DSSD(nn.Module):
    def __init__(self, phase: str, block: nn.Module, num_blocks: list, size=300, num_classes=2):
        super.__init__(Context_DSSD, self).__init__()
        self.num_blocks = num_blocks
        self.block = block
        self.phase = phase
        self.num_classes = num_classes
        self.priorbox = PriorBoxLayer(size, size, stride=[])
        self.priors = None
        self.priorbox_context = PriorBoxLayer(size, size, stride=[])
        self.priors_context = None

        self.size = size
        self.in_planes = 64

        # 先利用大核获得卷积特征，获取大感受野下的初步特征
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)

        # 下采样层
        self.layer1 = self._make_layer(block, 64, num_blocks[0], stride=1)
        self.layer2 = self._make_layer(block, 128, num_blocks[1], stride=2)
        self.layer3 = self._make_layer(block, 256, num_blocks[2], stride=2)



    def _make_layer(self, block, planes, num_blocks, stride):
        strides = [stride] + [1]*(num_blocks-1)     # [stride, 1, 1...(num_blocks-1)]
        layers = []
        for stride in strides:
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)



