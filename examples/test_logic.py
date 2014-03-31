#!/usr/bin/env python
import sys
sys.path.append('/Users/johntracey/Desktop/pyvafm-master/src')
from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_Logic


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	#Add Circuits
	machine.AddCircuit(type='square',name='s1', amp=1, freq=1, duty=0.5, pushed=True )
	machine.AddCircuit(type='square',name='s2', amp=1, freq=2.5, duty=0.2, pushed=True )
  	
	machine.AddCircuit(type='NOT',name='not', pushed=True )
	machine.AddCircuit(type='AND',name='and', pushed=True )
	machine.AddCircuit(type='OR',name='or', pushed=True )
	machine.AddCircuit(type='XOR',name='xor', pushed=True )
	machine.AddCircuit(type='NOR',name='nor', pushed=True )
	
	machine.Connect("s1.out","not.signal")
	machine.Connect("s1.out","and.in1","or.in1","xor.in1","nor.in1")
	machine.Connect("s2.out","and.in2","or.in2","xor.in2","nor.in2")
	
	
	out1 = machine.AddCircuit(type='output',name='output',file='test_logic.log', dump=1)
	out1.Register('global.time', 's1.out', 's2.out','not.out','and.out','or.out','xor.out','nor.out')
	
	for i in range(1000):
	    machine.Update()

	

if __name__ == '__main__':
	main()
