# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 09:52:56 2013

@author: Thomas Stolz
"""

from ctypes import *
from WLMconstants import *

class WLMError(Exception):
    def __init__(self, message):
        Exception(self, message)

class WavelengthMeter:
    def __init__(self):
        self.dll=windll.wlmData
        # start wlm if not running, using a timeout of 10 seconds and extended return information
        res = self.dll.ControlWLMEx(cCtrlWLMHide+cCtrlWLMWait, 0, 0, 10, 1)
        print hex(res)        
        if res>=flErrUnknownError:
            print 'Unknown Error'
            res-=flErrUnknownError
        if res>=flErrTemperatureError:
            print 'Temperature Error - unable to report correct measurements'
            res-=flTemperatureError
        if res>=flErrUnknownSN:
            print 'Unknown Serial Number'
            res-=flErrUnknownSN
        if res>=flErrWrongSN:
            print 'Wrong Serial Number'
            res-=flErrWrongSN
        if res>=flErrUnknownDeviceError:
            print 'Unknown Device Error'
            res-=flErrUnknownDeviceError
        if res>=flErrUSBError:
            print 'USB Error'
            res-=flErrUSBError     
        if res>=flErrDriverError:
            print 'Driver Error'
            res-=flErrDriverError
        if res>=flErrDeviceNotFound:
            print 'Device Not Found'
            res-=flErrDeviceNotFound   
        if res>=flServerStarted:
            print 'High Finesse Wavelength Meter started successfully'
            res-=flServerStarted
        else:
            raise WLMException('Unable to start server')
        if res==0:
            return
        else:     
            print 'Unknown Message'
    
    def getWL(self):
        getWL=self.dll.GetWavelength
        getWL.restype = c_double
        return getWL(c_double(0))         
