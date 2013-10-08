# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 14:45:02 2013

@author: universe
"""
import visa

class SC10:
    
    def __init__(self, address):
        self.device=visa.instrument(address, term_chars='\r', timeout=0.1)
        self.address=address
    def close(self):
        self.device.close()
    def reset(self, address=None):
        self.close()
        if not address:
            address=self.address
        self.__init__(address) 
    def ask(self, query):
        self.device.write(query+"\r")
        string=''
        while(True):
            try:
                new=self.device.read()
            except:
                break
            if (new=='>'):
                break
            new+='\r'
            string+=new
        #string=string.strip(query+'\r')
        #string=string.split('\r')
        result=string
        return result
    def toggle_enable(self):
        return self.ask("ens")
    def get_enable(self):
        "0 if disabled, 1 if enabled"
        return self.ask("ens?")
    def enable(self):
        if self.get_enable()=='ens?\r0\r':
            self.toggle_enable()
        else:
            pass
    def disable(self):
        if self.get_enable()=='ens?\r1\r':
            self.toggle_enable()
        else:
            pass
    def set_repeat_count(self,n):
        "repeat count for repeat mode (1-99)"
        return self.ask(str("rep=%d",n))
    def get_repeat_count(self):
        return self.ask("rep?")
    def set_op_mode(self,n):
        '''
        1 = manual 
        2 = auto
        3 = single
        4 = repeat
        5 = external
        '''
        return self.ask("mode=%d"%(n))
    def get_op_mode(self):
        '''
        1 = manual 
        2 = auto
        3 = single
        4 = repeat
        5 = external
        '''
        return self.ask("mode?")
    def set_trig_mode(self,n):
        "0 = internal, 1 = external"
        return self.ask("trig=%d"%(n))
    def get_trig_mode(self):
        return self.ask("trig?")
    def set_extrig_mode(self,n):
        "0: TTL follows shutter output, 1: TTL follows controller output"
        return self.ask("xto=%d"%(n))
    def get_extrig_mode(self):
        return self.ask("xto?")
    def set_open_time(self,n):
        "in ms"
        return self.ask("open=%d"%(n))
    def get_open_time(self):
        return self.ask("open?")
    def set_shut_time(self,n):
        "in ms"
        return self.ask(str("shut=%d",n))
    def get_shut_time(self):
        return self.ask("shut?")
    def get_closed_state(self):
        "0 = open, 1 = closed"
        return self.ask("closed?")
    def set_baud(self,n):
        "0: 9600 baud, 1: 115000 baud"
        return self.ask(str("baud=%d",n))
    def save_mode(self):
        "save baud rate and output trigger mode"
        return self.ask("save")
    def save_conf(self):
        "save ex. mode, open & shut time to EEPROM"
        return self.ask("savp")
    def load_conf(self):
        "load settings from EEPROM"
        return self.ask("resp")
    
        
    
            