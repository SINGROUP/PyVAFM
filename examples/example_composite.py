#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_math


def ADC(compo,**keys):
	
  	compo.AddInput("signal1")
  	compo.AddInput("signal2")
  	compo.AddOutput("out")
  	compo.AddCircuit(type='opAdd',name='adder',factors=2, pushed=True)
  	compo.Connect("global.signal1","adder.in1")
  	compo.Connect("global.signal2","adder.in2")
  	compo.Connect("adder.out","global.out")
	
	print "ADC assemb led!"

def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	
	#Add Circuits
	
	
  	osc = machine.AddCircuit(type='waver',name='osc', amp=1, freq=1, pushed=True )
  	
  	compo1 = machine.AddCircuit(type='Machine', name='compo1', assembly=ADC, pushed=True)
  	
	out1 = machine.AddCircuit(type='output',name='output',file='example_composite.log', dump=1)
	out1.Register('global.time', 'osc.sin', 'osc.cos', 'compo1.out')
	
	machine.Connect("osc.sin","compo1.signal1")
	machine.Connect("osc.cos","compo1.signal2")
	
	machine.Wait(10)
	
	#print compo1.I.keys()
	#print compo1.cCoreID
	#print machine.cCoreID
	
	#machine.cCore.DebugCircuit(osc.cCoreID);
	#machine.cCore.DebugCircuit(compo1.cCoreID);
	#machine.cCore.DebugCircuit(7);
	

if __name__ == '__main__':
	main()
