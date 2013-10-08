# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 11:06:55 2013

@author: universe
"""

import visa

class PM100A:

    def __init__(self, address):
        self.address=address
    def measPow(self):
        return float(self.device.ask('MEAS:POW?'))
    def start(self):
        self.device= visa.instrument(self.address)
    def close(self):
        self.device.close()
    def setAvCnt(self,cnt):
        self.device.write('SENS:AVER:COUN '+str(cnt))

PMeter=PM100A('USB0::0x1313::0x8079::P1000771::0::INSTR')