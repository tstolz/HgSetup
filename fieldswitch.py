# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 13:13:13 2013

@author: universe
"""
import serial
class fieldswitch():
    def __init__(self,port='COM7'):
        self.ser = serial.Serial(port, 9600, timeout=1)
        
    def closePort(self):
        try:
            self.ser.close()
        except: pass

    def polfieldOn(self):
        self.ser.write('1')
    
    def HoldingfieldOn(self):
        self.ser.write('2')
    
    def AllOff(self):
        self.ser.write('0')
