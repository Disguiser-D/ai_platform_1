#!/usr/bin/env python
import sys
import argparse
import os
import configparser

import tensorflow as tf
import numpy as np

from model import OpenNsfwModel, InputType
from image_utils import create_tensorflow_image_loader
from image_utils import create_yahoo_image_loader
from multiprocessing import Pool
import multiprocessing

IMAGE_LOADER_TENSORFLOW = "tensorflow"
IMAGE_LOADER_YAHOO = "yahoo"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cf = configparser.ConfigParser()
cf.read(os.path.join(BASE_DIR, 'config.ini'))
PROCESS_NUMBER = int(cf.get("Operational-configuration", "PROCESS_NUMBER"))
INPUT_TYPE = cf.get("Operational-configuration", "INPUT_TYPE")
FN_LOAD_IMAGE = cf.get("Operational-configuration", "FN_LOAD_IMAGE")

fn_load_image = None
if INPUT_TYPE == 'TENSOR':
    if FN_LOAD_IMAGE == IMAGE_LOADER_TENSORFLOW:
        fn_load_image = create_tensorflow_image_loader(tf.Session(graph=tf.Graph()))
    elif FN_LOAD_IMAGE == IMAGE_LOADER_YAHOO:
        fn_load_image = create_yahoo_image_loader()
    else:
        print("parameter error")
elif INPUT_TYPE == 'BASE64_JPEG':
    if FN_LOAD_IMAGE == IMAGE_LOADER_YAHOO:
        print("parameter mismatch")
    elif FN_LOAD_IMAGE == IMAGE_LOADER_TENSORFLOW:
        import base64

        fn_load_image = lambda filename: np.array([base64.urlsafe_b64encode(open(filename, "rb").read())])
    else:
        print("parameter error")
else:
    print("parameter error")

model = OpenNsfwModel()
input_type = InputType[INPUT_TYPE]
model.build(weights_path=os.path.join(BASE_DIR, 'open_nsfw-weights.npy'), input_type=input_type)
sess = tf.Session()
sess.run(tf.global_variables_initializer())


def process_start(data):
    image = fn_load_image(data)
    predictions = \
        sess.run(model.predictions,
                 feed_dict={model.input: image})
    res = {}
    str_tmp = "{} {}".format(*predictions[0]).encode()
    res_tmp = str_tmp.split()
    res['sfw_score'] = res_tmp[0]
    res['nsfw_score'] = res_tmp[1]

    return res
