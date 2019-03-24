from __future__ import division
import torch
from math import sqrt as sqrt


class PriorBoxLayer(object):
    """Compute priorbox coordinates in center-offset form for each source
    feature map.
    Note:
    This 'layer' has changed between versions of the original SSD
    paper, so we include both versions, but note v2 is the most tested and most
    recent version of the paper.

    """

    def __init__(self, width, height, stride=[4, 8, 16, 32, 64, 128], box=[16, 32, 64, 128, 256, 512],
                 scale=[1, 1, 1, 1, 1, 1], aspect_ratios=[[], [], [], [], [], []]):
        """
        initialize the prior box layer, use to create prior box
        :param width: the width of origin image
        :param height: the height of origin image
        :param stride: the stride list of different layers' feature map
        :param box: the box size of different layers' feature map
        :param scale: the box scale
        :param aspect_ratios: if not none, the box will has aspect ratios
        """
        super(PriorBoxLayer, self).__init__()
        self.width = width
        self.height = height
        self.stride = stride
        self.box = box
        self.scales = scale
        self.aspect_ratios = aspect_ratios

    def forward(self, prior_idx, f_width, f_height):
        """
        get prior box of different feature map
        :param prior_idx: the id of parameter
        :param f_width: the width of feature map
        :param f_height: the height of feature map
        :return: a tenor of (f_width*f_height, 4)
        """
        mean = []

        for i in range(f_height):
            for j in range(f_width):
                for scale in range(self.scales[prior_idx]):  # if scales == 1 then scale = 0 only
                    box_scale = (2 ** (1 / 3)) ** scale
                    cx = (j + 0.5) * self.stride[prior_idx] / self.width
                    cy = (i + 0.5) * self.stride[prior_idx] / self.height
                    side_x = self.box[prior_idx] * box_scale / self.width
                    side_y = self.box[prior_idx] * box_scale / self.height
                    mean += [cx, cy, side_x, side_y]

                    for ar in self.aspect_ratios[prior_idx]:
                        mean += [cx, cy, side_x / sqrt(ar), side_y * sqrt(ar)]
        output = torch.Tensor(mean).view(-1, 4)  # (f_height * f_width, 4)
        return output
