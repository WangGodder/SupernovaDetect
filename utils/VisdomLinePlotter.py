# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : Godder
from visdom import Visdom
import numpy as np


class VisdomLinePlotter(object):
    """Plots to Visdom"""
    def __init__(self, env_name='line env'):
        self.viz = Visdom()
        self.env = env_name
        self.plots = {}

    def plot(self, title_name: str, var_names: list or str, x, y, xlabel='Epochs', ylabel=None):
        if not isinstance(var_names, list):
            var_names = [var_names]
        if title_name not in self.plots:
            self.plots[title_name] = self.viz.line(X=np.array([x,x]), Y=np.array([y,y]), env=self.env, opts=dict(
                legend=var_names,
                title=title_name,
                xlabel=xlabel,
                ylabel=ylabel,
            ))
        else:
            self.viz.line(X=np.array([x]), Y=np.array([y]), env=self.env, win=self.plots[title_name], update='append', opts=dict(showlegend=True))
            # self.viz.line(X=np.array([x]), Y=np.array([y]), env=self.env, win=self.plots[title_name], name=var_names[0])

    # @Deprecated
    # def plot(self, var_name, split_name, x, y):
    #     if var_name not in self.plots:
    #         self.plots[var_name] = self.viz.line(X=np.array([x,x]), Y=np.array([y,y]), env=self.env, opts=dict(
    #             legend=[split_name],
    #             title=var_name,
    #             xlabel='Epochs',
    #             ylabel=var_name
    #         ))
    #     else:
    #         self.viz.updateTrace(X=np.array([x]), Y=np.array([y]), env=self.env, win=self.plots[var_name], name=split_name)
