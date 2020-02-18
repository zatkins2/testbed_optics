#!/usr/bin/python3

import numpy as np
import serial
import csv
import time 
import sys

# Helper functions

def cwrite(cmd, term = "\r\n".encode("utf-8"), delay = 1.0, comm = None):
    cmd = cmd.encode("utf-8")
    comm.write(cmd + term)
    time.sleep(delay)

def cread(comm = None):
    return comm.read(256).strip().decode("utf-8")

if __name__ == "__main__":
    
    # Comms parameters

    port = '/dev/' + sys.argv[1] 
    print(port)
    baud = 1200
    parity = serial.PARITY_ODD
    bytesize = serial.SEVENBITS
    cmddelay = 2.0
    timeout = 2.0
    term = "\r\n".encode("utf-8")

    # Data parameters

    fieldnames = ["t", "Sensor V [V]", "Control T [K]", "Control V [V]", "Heater Range [a.u.]", "Heater % [a.u.]", "Setpoint T [K]"]
    commands = [["SUNI S"], ["CUNI K"], ["CUNI S"], [], [], ["CUNI K"]]
    queries = ["SDAT?", "CDAT?", "CDAT?", "RANG?", "HEAT?", "SETP?"]

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

    # Do stuff

    print('Comm Active:',comm.is_open)

    with open(csv_name, "w", newline = "") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
       
    while True:

        with open(csv_name, "a", newline = "") as csvfile:
            
            writer = csv.DictWriter(csvfile, fieldnames)

            line = dict()
            line[fieldnames[0]] = time.time()

            for i in range(len(queries)):
                for j in range(len(commands[i])):
                    cwrite(commands[i][j], term = term, delay = cmddelay, comm = comm)
                cwrite(queries[i], term = term, delay = cmddelay, comm = comm)
                line[fieldnames[i + 1]] = cread(comm = comm)
        
            writer.writerow(line)

    comm.close()
    time.sleep(0.1)
    print('Comm Active:',comm.is_open)
