# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 09:52:56 2013

@author: Thomas Stolz
"""

from ctypes import *
from WLMconstants import *
import time

class WLMError(Exception):
    def __init__(self, message):
        Exception(self, message)

class WavelengthMeter:
    def __init__(self):
        self.dll=windll.wlmData
        
        #self.dll.Instantiate(cInstCheckForWLM, 0,0,0)
        
        # start wlm if not running, using a timeout of 10 seconds and extended return information
        res = self.dll.ControlWLMEx(cCtrlWLMHide+cCtrlWLMStartSilent+cCtrlWLMWait, 0, 0, 10000, 1)
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
            raise WLMError('timeout - unable to start server')
        if res==0:
            return
        else:     
            print 'Unknown Message'
        
    def getWL(self):
        getWL=self.dll.GetWavelength
        getWL.restype = c_double
        self.dll.TriggerMeasurement(cCtrlMeasurementContinue)
        return getWL(c_double(0))
    def setExpMode(self, autotrue):
        setMode=self.dll.SetExposureMode
        setMode(c_bool(autotrue))
    def showApp(self):
        self.dll.ControlWLM(cCtrlWLMShow,0,0)
    def startMeasurement(self):
        self.dll.Operation(cCtrlStartMeasurement)
    def stopMeasurement(self):
        self.dll.Operation(cCtrlStopAll)
    def setContinuous(self):
        self.dll.SetPulseMode(0)
    
            
#SUGGESTED SETTINGS:
#W=WavelengthMeter()
#W.showApp()
#W.setExpMode(True)
#W.setContinuous()
#W.startMeasurement()
