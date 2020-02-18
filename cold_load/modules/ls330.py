#!/usr/bin/python3

import numpy as np
import serial
import csv
import time 
import sys
import os

# Helper functions

def cwrite(cmd, term = "\r\n".encode("utf-8"), delay = 1.0, comm = None):
    cmd = cmd.encode("utf-8")
    comm.write(cmd + term)
    time.sleep(delay)

def cread(comm = None):
    return comm.read(256).strip().decode("utf-8")

def htr_bool_exists(path, name = "htr_bool_arr.npy"):
    return os.path.exists(path + name)

def write_htr_bool(init, path, name = "htr_bool_arr.npy"):
    if type(init) != 'bool':
        raise ValueError("init must be bool type")
    np.save(path + name, init)
    return

def read_htr_bool(path, name = "htr_bool_arr.npy"):
    return np.load(path + name)
