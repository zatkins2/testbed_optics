#!/usr/bin/python3

import numpy as np
import serial
import time 
import csv

import sys
import os

class ls336:
    '''
    Implements a lakeshore 336 box to interface with client scripts. Only contains locally relevant information; namely, port parameters. The state of the device is not stored locally to avoid the potential for inconsistent information. Device status can always be accessed (accurately) through a query.    
    '''

    #Class variables
    
    baud = 57600
    bytesize = serial.SEVENBITS
    parity = serial.PARITY_ODD
    stopbits = serial.STOPBITS_ONE
    timeout = 1.0
    term = '\r\n'
    std_delay = 0.05

    #Constructor and instance variables

    def __init__(self, port):
        '''
        Creates a new lakeshore device, located at local port 'port'.

        Parameters
        ------
        port : str
            Absolute path to port containing the device, e.g. '/dev/ttyUSB0'.

        Returns
        ------
        out : ls336 object
            An instance of the ls336 class of objects, i.e. a lakeshore 336 device.
        '''

        self.port = port
        self.comm = serial.Serial(port, self.baud, self.bytesize, self.parity, self.stopbits, self.timeout)
        self.comm.close()

    #Instance methods

    def write(self, cmd, delay = std_delay, stay_open = False):
        r'''
        Writes character string cmd to port comm, including commands and queries.

        Parameters
        ------
        comm : serial.Serial object
            The port on the local machine attached to the device. See pyserial documentation. Must be configured according to the lakeshore manual.

        cmd : string
            The character sequence to send to the device. Must be in the device proprietary library, available in the lakeshore manual.

        delay : float or int
            After writing, the function will lock out the kernel for delay seconds. Within a script, this prevents too many cmds being written to the device too quickly.

        term : str
            Terminating character sequence appended to cmd. Indicates end of message.
        '''
        
        if not self.comm.is_open:
            self.comm.open()

        cmd = cmd + self.term
        cmd = cmd.encode()
        self.comm.write(cmd)
        
        if not stay_open:
            self.comm.close()
        
        time.sleep(delay)

    def read(self, size = None):
        r'''
        Reads data from the device attached to port comm. Implemented via pyserial 'read_until' command: reads until receives '\n'; every lakeshore response terminates with '\r\n'.

        Parameters
        ------
        comm : serial.Serial object
            The port on the local machine attached to the device. See pyserial documentation. Must be configured according to the lakeshore manual.
        
        size : int, optional
            Number of bytes to read. If provided, may be less than full message length.
        
        Returns
        ------
        out : str
            Message from lakeshore device.
        '''        
      
        if not self.comm.is_open:
            self.comm.open()
        
        out = self.comm.read_until(size = size).strip().decode()
        self.comm.close()
        return out

    def read_size(self, size = 256):
        r'''
        Reads data from the device attached to port comm. Implemented via pyserial 'read' command: reads until receives size bytes.

        Parameters
        ------
        comm : serial.Serial object
            The port on the local machine attached to the device. See pyserial documentation. Must be configured according to the lakeshore manual.
        
        size : int, optional
            Number of bytes to read. If provided, may be less than full message length.
        
        Returns
        ------
        out : str
            Message from lakeshore device.
        '''        
        
        if not self.comm.is_open:
            self.comm.open()
        
        out = self.comm.read(size = size).strip().decode()
        self.comm.close()
        return out

    def query(self, cmd, delay = std_delay, write_kwargs = dict(delay = 0, stay_open = True), read_kwargs = dict()):
        r'''
        Packages query command strings with a call to read, which minimizes port-usage time.

        Parameters
        ------
        comm : serial.Serial object
            The port on the local machine attached to the device. See pyserial documentation. Must be configured according to the lakeshore manual.

        cmd : string
            The character sequence to send to the device. Must be in the device proprietary library, available in the lakeshore manual.
        
        delay : float or int
            After writing and reading, the function will lock out the kernel for delay seconds. Within a script, this prevents too many cmds being written to the device too quickly.

        write_kwargs : dict
            dict of kwargs to pass to the write function.

        read_kwargs : dict
            dict of kwargs to pass to the read function.

        Returns
        ------
        out : str
            Message from lakeshore device.
        '''

        self.write(cmd, **write_kwargs)
        out = self.read(**read_kwargs)

        time.sleep(delay)
        
        return out

    def write_setp(self, output, val):
        r'''
        Wrapper for 'SETP' hardware method. 

        Parameters
        ------
        See lakeshore manual.
        '''
        
        if output not in [1, 2, 3, 4]:
            raise ValueError(f'invalid output in write_setp: {output}')

        self.write(f'SETP {output} {val}')

    def query_setp(self, output):
        r'''
        Wrapper for 'SETP?' hardware method. 

        Parameters
        ------
        See lakeshore manual.
        '''
        
        if output not in [1, 2, 3, 4]:
            raise ValueError(f'invalid output in query_setp: {output}')

        return self.query(f'SETP? {output}')

    def write_htr_range(self, output, val):
        r'''
        Wrapper for 'RANGE' hardware method. 

        Parameters
        ------
        See lakeshore manual.
        '''
        
        if output not in [1, 2, 3, 4]:
            raise ValueError(f'invalid output in write_htr_range: {output}')

        self.write(f'RANGE {output} {val}')
        
    def query_htr_range(self, output):
        r'''
        Wrapper for 'RANGE?' hardware method. 

        Parameters
        ------
        See lakeshore manual.
        '''
        
        if output not in [1, 2, 3, 4]:
            raise ValueError(f'invalid output in query_htr_range: {output}')

        return self.query(f'RANGE? {output}')

    def query_htr_lvl(self, output):
        r'''
        Wrapper for 'HTR?' hardware method. 

        Parameters
        ------
        See lakeshore manual.
        '''
        
        if output not in [1, 2]:
            raise ValueError(f'invalid output in query_htr_lvl: {output}')

        return self.query(f'HTR? {output}')

    def query_kelvin(self, inp):
        r'''
        Wrapper for 'KRDG?' hardware method. 

        Parameters
        ------
        See lakeshore manual.
        '''
        
        if inp not in [0, 'a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']:
            raise ValueError(f'invalid input in query_kelvin: {inp}')

        return self.query(f'KRDG? {inp}')
        
    def query_sensor(self, inp):
        r'''
        Wrapper for 'SRDG?' hardware method. 

        Parameters
        ------
        See lakeshore manual.
        '''
        
        if inp not in [0, 'a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']:
            raise ValueError(f'invalid input in query_sensor: {inp}')

        return self.query(f'SRDG? {inp}')

# Do stuff

if __name__ == '__main__':

    # Initialize device

    box = ls336('/dev/ttyUSB0')

    # Ask basic questions
    
    print('Comm Active:', box.comm.is_open)
    print(box.query('*IDN?'))
    print(box.query_kelvin(0))
    print(box.query_setp(1))
    print(box.query_htr_lvl(1))
    box.comm.close()
    print('Comm Active:', box.comm.is_open)
