# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : Godder
# @Github  : https://github.com/WangGodder
import torch
import torch.nn as nn
import torch.nn.functional as F
from .layer import PriorBoxLayer


class Context_DSSD(nn.Module):
    def __init__(self, phase, block, num_blocks, size=300, num_classes=2):
        super.__init__(Context_DSSD, self).__init__()
        self.phase = phase
        self.num_classes = num_classes
        self.priorbox = PriorBoxLayer(size, size, stride=[])
        self.priors = None
        self.priorbox_context = PriorBoxLayer(size, size, stride=[])
        self.priors_context = None

        self.size = size





