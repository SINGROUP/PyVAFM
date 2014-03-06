#!/usr/bin/env python

#from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_control
#import vafmcircuits_math
import vafmcircuits_Filters


def main():
    
    machine = Machine(name='machine', dt=0.01, pushed=True);
    
    machine.AddCircuit(type='waver',name='osc', freq=1, pushed=True)
    machine.AddCircuit(type='opAbs',name='abs', pushed=True)
    machine.AddCircuit(type='SKLP',name='lp', fcut=0.04, pushed=True)
    
    #pi = machine.AddCircuit(type='PI', name='pi', set=1,Kp=1.5,Ki=0.2)
    pid = machine.AddCircuit(type='PID', name='pi', set=1,Kp=1.5,Ki=0.2,Kd=0.1)
    
    machine.Connect("osc.sin","abs.signal")
    machine.Connect("abs.out","lp.signal")
    
    machine.Connect("lp.out","pi.signal")
    machine.Connect("pi.out","osc.amp")
    
    out1 = machine.AddCircuit(type='output',name='output',file='test_pi.log', dump=5)
    out1.Register('global.time', 'osc.sin', 'lp.out', 'pi.out')
    
    machine.Wait(100)
	

if __name__ == '__main__':
	main()

