##!/usr/bin/env python
import subprocess
import sys
sys.path.append('/Users/johntracey/Desktop/pyvafm-master/src')

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits



	
#main machine
machine = Machine(name='machine', dt=0.0001, pushed=True)
	
# wave generator
machine.AddCircuit(type='waver',name='wave', amp=1, freq=2, phi=1, offset=2.0, pushed=True)
machine.AddCircuit(type='square',name='sqw', amp=1.5, freq=2, offset=0.0, duty=0.2, pushed=True )
machine.AddCircuit(type='opAdd',name='Add', pushed=True )

machine.Connect("wave.sin","Add.in1")	
machine.Connect("wave.sin","Add.in2")	

#output to file - dump=0 means only manual dump
out1 = machine.AddCircuit(type='output',name='output',file='wavers.log', dump=1)
out1.Register('global.time', 'wave.sin', 'wave.cos', 'wave.saw', 'sqw.out',"Add.out")
	
	
machine.Wait(1)
	

