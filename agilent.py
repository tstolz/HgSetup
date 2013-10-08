import visa
import time

#polfield GPIB 4
#holding field: GPIB 5
#AOM 192.168.1.121

class Agilent33521A:
    def __init__(self,ipAdress=None):
        self.ip=ipAdress
        self.device=visa.instrument("TCPIP::"+self.ip+"::INSTR")
        self.connection_type='LAN'
    def reset(self):
        self.write('*RST')
    def write(self,string):
        self.device.write(string)
    def read(self):
        return self.device.read()
    def setSin(self):
        self.write('SOUR:FUNC SIN')
    def setSquare(self):
        self.write('SOUR:FUNC SQU')
    def setDC(self,val):
        self.write('SOUR:APPL:DC DEF, DEF, '+str(val))
    def setPulse(self):
        self.write('SOUR:FUNC PULS ')
    def setVoltageOffset(self, amp):
        self.write('SOUR:VOLT:OFFS '+str(amp))
    def setVoltage(self, val):
        self.write('SOUR:VOLT '+str(val))
    def setPulseDCYC(self, percent):
        self.write('SOUR:FUNC:PULS:DCYC '+str(percent))
    def setPulsePeriod(self, sec):
        self.write('SOUR:FUNC:PULS:PER '+str(sec))
    def syncON(self):
        self.write('OUTP:SYNC ON')
    def syncOFF(self):
        self.write('OUTP:SYNC OFF')
    def outputON(self):
        self.write('OUTP ON')
    def outputOFF(self):
        self.write('OUTP OFF')
    def setTrigRemote(self):
        self.write('TRIG:SOUR BUS')
    def setTrigExt(self):
        self.write('TRIG:SOUR EXT')
    def setTrigSlope(self, rise):
        'rising slope if true'
        if rise:
            slop='POS'
        else:
            slop='NEG'
        self.write('TRIG:SLOP '+slop)
    def trig(self):
        self.write('*TRG')
    def burstON(self):
        self.write('BURS:STAT ON')
    def burstOFF(self):
        self.write('BURSt:STATe OFF')
    def burstNcyc(self, ncyc):
        self.write('BURS:NCYC '+str(ncyc))
    def burstTrigMode(self, mode): 
        '''valid: 'TRIG' for triggered and 'GAT' for gated'''
        self.write('BURS:MODE '+mode)
    def burstPeriod(self, period):
        '''parameter: period in s'''
        self.write('BURS:INT:PER '+str(period))
    def highLevV(self, voltage):
        self.write('VOLT:HIGH '+str(voltage))
    def lowLevV(self, voltage):
        self.write('VOLT:LOW '+str(voltage))
    def outputINV(self,yes):
        'True for inverse, False for normal'
        if yes:
            val='INV'
        else:
            val='NORM'
        self.write('OUTP:POL '+val)
    def syncINV(self,yes):
        'True for inverse, False for normal'
        if yes:
            val='INV'
        else:
            val='NORM'
        self.write('OUTP:SYNC:POL '+val)
    def readErr(self):
        self.write('SYST:ERR?')
        return self.read()
    

class Agilent3645A:
    def __init__(self,visaGPIBAdress=5):
        self.GPIB="GPIB::"+str(visaGPIBAdress)
        self.device=visa.instrument(self.GPIB)
        self.write('*RST')
    def write(self,string):
        self.device.write(string)
    def read(self):
        return self.device.read()
    def setVoltage(self,voltage):
        self.write('APPL '+str(voltage)+', MAX')
    def setCurrent(self,current):
        self.write('APPL MAX, '+str(current))
    def setVoltCurr(self,voltage, current):
        self.write('APPL '+str(voltage)+', '+str(current))
    def outputON(self):
        self.write('OUTP ON')
    def outputOFF(self):
        self.write('OUTP OFF')
    def rampUP(self,rampTo,rampTime,StepSize=None):
        """ramp current up from current value to rampTo (A)"""
        self.write('CURR?')#get current current setting
        current=float(self.read())
        if current>rampTo:
            print "value to ramp to is smaller then current setting"    
            return
        self.write('CURR:STEP DEF')
        self.write('CURR:STEP? DEF')
        if StepSize:
            step=StepSize
            self.write('CURR:STEP '+str(StepSize))
        else:
            step=float(self.read())
        steps=int(((rampTo-current)/step))
        steptime=float(rampTime)/steps
        for i in range(steps):
            self.write("CURR UP")
            time.sleep(steptime)
    def rampDOWN(self, rampTime, StepSize=None):
        """Ramp current to 0, Stepsize in Ampere or "DEF" for minimum res step"""
        self.write('CURR?')
        current=float(self.read())
        if StepSize:
            step=StepSize
            self.write('CURR:STEP '+str(StepSize))
        else:
            step=float(self.read())
        steps=int((current/step))-1
        steptime=float(rampTime)/steps
        for i in range(steps):
            self.write("CURR DOWN")
            time.sleep(steptime)
        self.write('CURR?')
        current=float(self.read())
        if current>step:
            return "residual current larger than stepsize"
        self.write("CURR 0.")#because stepping can not go to 0 it seems
class Agilent332208:
    def __init__(self,ipAdress=None):
        self.ip=ipAdress
        self.device=visa.instrument("TCPIP::"+self.ip+"::INSTR")
        self.connection_type='LAN'
        self.write('*RST')
    def write(self,string):
        self.device.write(string)
    def read(self):
        return self.device.read()
    def setSin(self,freq,amp,off):
        self.write('APPL:SIN '+str(freq)+', '+str(amp)+', '+str(off))
    def setSquare(self,freq,amp,off):
        self.write('APPL:SQU '+str(freq)+', '+str(amp)+', '+str(off))
    def setDC(self,val):
        self.write('APPL:DC DEF, DEF, '+str(val))
    def setDutyCyc(self,percent):
        self.write('FUNC:SQU:DCYC '+str(percent))
    def uploadUserSignal(self, data):
        ''' "data" must be a list containing integers in the range -8191 to +8191, max. length 65536 '''
        self.write('DATA:DAC VOLATILE, '+str(data)[1:-1]) 
    def saveUserSignal(self, name):
        ''' "name" must be a string of max. length 12 containing letters (A-Z), numbers (0-9) or "_", first entry letter (A-Z)'''
        if not self.checkFree():
            self.deleteALL
        self.write('DATA:COPY '+str(name)+', VOLATILE')
    def deleteALL(self):
        self.write('DATA:DEL:ALL')
    def checkFree(self):
        self.write('DATA:NVOL:FREE?')
        time.sleep(0.1)
        answer=self.read()
        if (answer=="0"): #insert correct answer
            return False
        else:
            return True
    def outputON(self):
        self.write('OUTP ON')
    def outputOFF(self):
        self.write('OUTP OFF')
    def setTrigRemote(self):
        self.write('TRIGger:SOURce BUS')
    def trig(self):
        self.write('*TRG')
    def burstON(self):
        self.write('BURS:STAT ON')
    def burstOFF(self):
        self.write('BURSt:STATe OFF')
    def burstNcyc(self, ncyc):
        self.write('BURS:NCYC '+str(ncyc))
    def burstTrigMode(self, mode): 
        '''valid: 'TRIG' for triggered and 'GAT' for gated'''
        self.write('BURS:MODE '+mode)
    def burstPeriod(self, period):
        '''parameter: period in s'''
        self.write('BURS:INT:PER '+str(period))
    def setPulse(self):
        #'''parameters: frequency, amplitude, offset'''
        #self.write('APPL:PULS '+str(freq)+str(ampl)+str(offset))
        self.write('FUNC PULS')
    def setPulsePeriod(self,sec):
        self.pulsPeriod(sec)
    def pulsPeriod(self, per):
        '''argument: period in s'''
        self.write('PULS:PER '+str(per))
    def pulsDcycle(self, dcyc):
        '''argument: dutycycle in s or 'MIN' or 'MAX' '''
        self.write('FUNC:PULS:DCYC '+str(dcyc))
    def highLevV(self, voltage):
        self.write('VOLT:HIGH '+str(voltage))
    def lowLevV(self, voltage):
        self.write('VOLT:LOW '+str(voltage))
    def outputINV(self,yes):
        'True for normal, False for inverse'
        if yes:
            val='INV'
        else:
            val='NORM'
        self.write('OUTP:POL '+val)

def transversPol(ipAdress, pulsetime, dutycycle, pulseAmp, constAmp, freq):
    A=Agilent332208(ipAdress)
    A.setSquare(freq, pulseAmp, pulseAmp/2)
    A.setDutyCyc(dutycycle)
    A.outputON()
    time.sleep(pulsetime)
    A.setDC(constAmp)
def transversPol2(ipAdress, pulsetime, dutycycle, pulseAmp, constAmp, freq, prectime):
    A=Agilent332208(ipAdress)
    A.setSquare(freq, pulseAmp, pulseAmp/2)
    A.setDutyCyc(dutycycle)
    A.outputON()
    time.sleep(pulsetime)
    A.outputOFF()
    time.sleep(prectime)
    A.setDC(constAmp)
    A.outputON()
def T1measNonRotated(PolFieldGPIBaddr, AOMipAdress, polCurrent, polTime, polLaseramp, readLaseramp, relaxtime, readtime):
    """
        T1 measurement routine
        using the helping coil to polarize AND store the polarization
    """
    polfield=Agilent3645A(PolFieldGPIBaddr)
    AOM=Agilent332208(AOMipAdress)
    polfield.setCurrent(polCurrent)
    AOM.setDC(polLaseramp)
    time.sleep(polTime)
    AOM.setDC(0)
    time.sleep(relaxtime)
    polfield.setCurrent(0)
    AOM.setDC(readLaseramp)
    time.sleep(readtime)
    
    
    
        
    

#transversPol('192.168.1.29',20,30,0.9,0.4,22.78) 
