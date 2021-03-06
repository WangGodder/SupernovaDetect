# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : Godder
# @Github  : https://github.com/WangGodder
import argparse
from models import Darknet
from utils.yolo_utils import *
from utils.parse_config import *
import torch
import os


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=30, help="number of epochs")
    parser.add_argument("--image_folder", type=str, default="data/samples", help="path to dataset")
    parser.add_argument("--batch_size", type=int, default=16, help="size of each image batch")
    parser.add_argument("--model_config_path", type=str, default="models/config/yolov3.cfg", help="path to model config file")
    parser.add_argument("--data_config_path", type=str, default="config/coco.data", help="path to data config file")
    parser.add_argument("--weights_path", type=str, default="weights/yolov3.weights", help="path to weights file")
    parser.add_argument("--class_path", type=str, default="data/coco.names", help="path to class label file")
    parser.add_argument("--conf_thres", type=float, default=0.8, help="object confidence threshold")
    parser.add_argument("--nms_thres", type=float, default=0.4, help="iou thresshold for non-maximum suppression")
    parser.add_argument("--n_cpu", type=int, default=0, help="number of cpu threads to use during batch generation")
    parser.add_argument("--img_size", type=int, default=416, help="size of each image dimension")
    parser.add_argument("--checkpoint_interval", type=int, default=1, help="interval between saving model weights")
    parser.add_argument(
        "--checkpoint_dir", type=str, default="checkpoints", help="directory where model checkpoints are saved"
    )
    parser.add_argument("--use_cuda", type=bool, default=True, help="whether to use cuda if available")
    return parser.parse_args()


if __name__ == '__main__':
    opt = arg_parser()
    print(opt)

    cuda = torch.cuda.is_available() and opt.use_cuda

    os.makedirs("output", exist_ok=True)
    os.makedirs("checkpoints", exist_ok=True)

    classes = load_classes(opt.class_path)

    # Get data configuration
    data_config = parse_data_config(opt.data_config_path)
    train_path = data_config["train"]

    # Get hyper parameters
    hyperparams = parse_model_config(opt.model_config_path)[0]
    learning_rate = float(hyperparams["learning_rate"])
    momentum = float(hyperparams["momentum"])
    decay = float(hyperparams["decay"])
    burn_in = int(hyperparams["burn_in"])

    # Initiate model
    model = Darknet(opt.model_config_path)
    # model.load_weights(opt.weights_path)
    model.apply(weights_init_normal)

    if cuda:
        model = model.cuda()

    model.train()

