import multiprocessing as mp

from traceback import print_exc

import traceback

import sys

from magic import process_image
import cv2 as cv
import glob
import os.path as path
import random
import numpy as np
import ctypes as c

height = 800
width = 800
images = 500
processes = 8
colorsegmentcount = 20


shared_output = None


def process(file):
    global shared_output
    output = np.frombuffer(shared_output.get_obj(), dtype=np.uint8)
    output = output.reshape((width, height, 4))
    process_image(file, output, width, height)


def asyncerror(e):
    print(e)
    print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)


def create_art(imagesdir, outputfile):
    global shared_output
    shared_output = mp.Array(c.c_uint8, width*height*4)

    with mp.Pool(processes=processes) as pool:
        files = glob.glob(imagesdir + "/*")

        tasklist = []

        if len(files) == 0:
            raise Exception("No media files found")

        for file in random.choices(files, k=images):
            if not path.exists(file):
                print("Hu? File does not exist: " + file)
                continue
            tasklist.append(pool.apply_async(process, args=(file, ), error_callback=asyncerror))

        for task in tasklist:
            task.wait(timeout=10)

        output = np.frombuffer(shared_output.get_obj(), dtype=np.uint8).reshape((width, height, 4))

        cv.imwrite(outputfile, output)
