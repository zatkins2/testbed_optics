#!/usr/bin/python3

import numpy as np
import serial
import csv
import time 
import sys
import os

sys.path.append('../modules/')

import ls336

if __name__ == "__main__":
    
    # Comms parameters

    port = '/dev/' + sys.argv[1] 

    # Initialize device

    box = ls336.ls336(port)

    # Fields

    fields = ["kelvin", "sensor", "htr_range 1", "htr_lvl 1", "setp 1"]
    field_args = [(0,), (0,), (1,), (1,), (1,)]
    field_kwargs = [{}, {}, {}, {}, {}]

    # Test fields

    if len(fields) != len(field_args):
        raise ValueError('len fields != len field_args')

    if len(fields) != len(field_kwargs):
        raise ValueError('len fields != len field_kwargs')

    for field in fields:
        getattr(box, 'query_' + field.split()[0])

    # Log parameters

    delay = 5

    # Initialize csv file

    t_name = time.localtime()
    csv_name = "../logs/"
    for i in range(6):
        csv_name += str(t_name[i]).zfill(2)
        if i == 2:
            csv_name += "_"
    csv_name += ".csv"

    # Start logging

    with open(csv_name, 'w', newline = '') as csvfile:
        writer = csv.DictWriter(csvfile, ['t'] + fields, delimiter = ';')
        writer.writeheader()
       
    while True:

        with open(csv_name, "a", newline = "") as csvfile:
            
            writer = csv.DictWriter(csvfile, ['t'] + fields, delimiter = ';')

            line = dict()
            line['t'] = time.time()

            for i in range(len(fields)):
                query = getattr(box, 'query_' + fields[i].split()[0])
                line[fields[i]] = query(*field_args[i], **field_kwargs[i])
        
            writer.writerow(line)
            time.sleep(delay)

    box.comm.close()
    time.sleep(0.1)
    print('Comm Active:',comm.is_open)
