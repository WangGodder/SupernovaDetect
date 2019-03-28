# -*- coding: utf-8 -*-
# @Time    : 2019/3/28
# @Author  : Godder
# @Github  : https://github.com/WangGodder
import logging
import time
import os


class TrainLogger(logging.Logger):
    def __init__(self, log_dir: str, console=True, file_time_formatter=None, log_train_formatter=None, log_warn_formatter=None):
        super(TrainLogger, self).__init__('trainLogger')
        self.file_time_formatter = file_time_formatter
        self.log_warn_formatter = log_warn_formatter
        self.log_train_formatter = log_train_formatter
        self.fileDir = log_dir
        self.console = console
        self.addHandler(self._create_info_handler())
        self.addHandler(self._create_warn_handler())
        self.setLevel(logging.INFO)

    def _create_info_handler(self):
        if not os.path.exists(self.fileDir):
            os.mkdir(os.path.dirname(self.fileDir))
        filename = time.strftime('%Y-%m-%d') if self.file_time_formatter is None else time.strftime(self.file_time_formatter)
        filename += '_train.log'
        handler = logging.FileHandler(os.path.join(self.fileDir, filename))
        formatter = logging.Formatter('%(asctime)s\t%(message)s')
        if self.log_train_formatter is not None:
            formatter = logging.Formatter(self.config['log_train_formatter'])
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        return handler

    def _create_warn_handler(self):
        filename = time.strftime('%Y-%m-%d') if self.file_time_formatter is None else time.strftime(self.file_time_formatter)
        filename += '_warn.log'
        handler = logging.FileHandler(os.path.join(self.fileDir, filename))
        formatter = logging.Formatter('%(asctime)s [line:%(lineno)d]\t%(message)s')
        if self.log_warn_formatter is not None:
            formatter = logging.Formatter(self.config['log_warn_formatter'])
        handler.setFormatter(formatter)
        handler.setLevel(logging.WARN)
        return handler

    def train_log(self, msg: str):
        self.info(msg)
        if self.console:
            print(msg)
