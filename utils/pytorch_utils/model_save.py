# -*- coding: utf-8 -*-
# @Time    : 2019/3/28
# @Author  : Godder
# @Github  : https://github.com/WangGodder
import time
import os
import torch
from torch import nn


def model_save(model, save_dir: str, epoch: int, best=False):
    """
    save pytorch Module to save dir and name file with time and epoch
    :param model: the model to save
    :param save_dir: the dir of save file
    :param epoch: the epoch of model
    :param best: whether model is the best current, the file name will be {time} + best
    :return: the message to log
    """
    if isinstance(model, torch.nn.DataParallel):
        real_model = model.module   # type: nn.DataParallel
    else:
        real_model = model          # type: nn.Module
    state = real_model.state_dict()
    for key in state:
        state[key] = state[key].clone().cpu()
    filename = time.strftime('%Y-%m-%d')
    if best:
        filename += '_best.pth'
    else:
        filename += '_' + str(epoch) + '.pth'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    torch.save(state, os.path.join(save_dir, filename))
    return "save model state dict with {} epochs in {}".format(epoch, os.path.join(save_dir, filename))


# if __name__ == '__main__':
#     model = Deep_HiTS()
#     load_state = torch.load('./checkpoint/2019-03-28_0.pth')
#     model.load_state_dict(load_state)
#     state = model.state_dict()
#     print(state)
    # model = torch.nn.DataParallel(model).cuda()
    # print(model_save(model, './checkpoint/', 0))
