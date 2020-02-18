#!/usr/bin/python3

import numpy as np
import serial
import csv
import time 
import sys
import os

sys.path.append('~/Users/zatkins/Cold-Load/modules/')
import ls330 as ls

run = False

if __name__ == "__main__" and run:
    
    # Comms parameters

    port = '/dev/' + sys.argv[1] 
    print(port)
    baud = 1200
    parity = serial.PARITY_ODD
    bytesize = serial.SEVENBITS
    cmddelay = 1.0
    timeout = 2.0
    term = "\r\n".encode("utf-8")

    # Data parameters

    fieldnames = ["t", "sensor_V", "control_T", "control_V", "heat_range", "heat_%"]
    commands = [["SUNI S"], ["CUNI K"], ["CUNI S"], [], []]
    queries = ["SDAT?", "CDAT?", "CDAT?", "RANG?", "HEAT?"]

    if len(commands) != len (queries):
        raise ValueError("len(commands) != len(queries), check data parameters")

    # Initialize device

    comm = serial.Serial(port, baud, bytesize, parity, timeout = timeout)

    # Initialize csv file

    t_name = time.localtime()
    csv_name = "../../logs/"
    for i in range(6):
        csv_name += str(t_name[i]).zfill(2)
        if i == 2:
            csv_name += "_"
    csv_name += ".csv"

    # Initialize heater running? variable

    htr_bool_path = "./" + os.path.stripext(os.path.basename(__file__))[0] + "_aux/"
    if not ls.htr_bool_exists(htr_bool_path):
        ls.write_htr_bool(False, htr_bool_path)

    # Do stuff

    print('Comm Active:',comm.is_open)

    with open(csv_name, "w", newline = "") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
       
    htr_flag = ls.read_htr_bool(htr_bool_path)   
    while True and not htr_flag:

        with open(csv_name, "a", newline = "") as csvfile:
            
            writer = csv.DictWriter(csvfile, fieldnames)

            line = dict()
            line[fieldnames[0]] = time.time()

            for i in range(len(queries)):
                for j in range(len(commands[i])):
                    ls.cwrite(commands[i][j], term = term, delay = cmddelay, comm = comm)
                ls.cwrite(queries[i], term = term, delay = cmddelay, comm = comm)
                line[fieldnames[i + 1]] = ls.cread(comm = comm)
        
            writer.writerow(line)

    comm.close()
    time.sleep(0.1)
    print('Comm Active:',comm.is_open)
