#!/usr/bin/python

import numpy as np
import serial
import time 

# Comms parameters

port = '/dev/ttyUSB0'
baud = 1200
parity = serial.PARITY_ODD
bytesize = serial.SEVENBITS
cmddelay = 0.6
timeout = 2.0
term = '\r\n'

# Initialize device

comm = serial.Serial(port, baud, bytesize, parity, timeout = timeout)

# Helper functions

def cwrite(cmd, comm = comm, delay = cmddelay):
  comm.write(cmd + term)
  time.sleep(delay)

def cread(comm = comm):
  return comm.read(100).strip()

# Do stuff

from time import sleep

print 'Comm Active:',comm.is_open
cwrite('CDAT?')
print "CDAT = " + cread()
cwrite("SDAT?")
print "SDAT = " + cread()
comm.close()
time.sleep(60)
print 'Comm Active:',comm.is_open
