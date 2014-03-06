#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_signal_processing


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	
	#Add Circuits
	
	
  	machine.AddCircuit(type='waver',name='w1', amp=0.2, freq=1, pushed=True )
  	machine.AddCircuit(type='waver',name='w2', amp=0.2, freq=1.15, pushed=True )
	machine.AddCircuit(type='phasor', name='lag', up=True, pushed=True)
	
	machine.Connect("w1.sin","lag.in1")
	machine.Connect("w2.cos","lag.in2")

	out1 = machine.AddCircuit(type='output',name='output',file='test_phasor.log', dump=5)
	out1.Register('global.time', "w1.sin","w2.cos","lag.tick","lag.delay")
	
	machine.Wait(10)

	

if __name__ == '__main__':
	main()

