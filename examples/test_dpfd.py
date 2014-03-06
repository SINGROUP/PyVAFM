#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine

#import vafmcircuits
#import vafmcircuits_control
#import vafmcircuits_Filters
from customs_pll import *


def main():
	
	f0=1.0e5
	
	machine = Machine(name='machine', dt=1.0e-8, pushed=True);
	
	machine.AddCircuit(type='waver',name='osc', amp=1, freq=f0+1.3, pushed=True)
	machine.AddCircuit(type='waver',name='vco', amp=1, freq=f0, pushed=True)
	machine.AddCircuit(type="Machine",name='pfd', assembly=dPFD, gain=1000.0, fcut=500, 
		KI=-0.0,KP=-0.30, pushed=True)
	
	machine.AddCircuit(type='opAdd',name='frq', in2=f0, pushed=True)
	
	'''
	machine.AddCircuit(type="DRFlipFlop",name="ff1", D=1, pushed=True)
	machine.AddCircuit(type="DRFlipFlop",name="ff2", D=1, pushed=True)
	machine.AddCircuit(type="AND",name="and", pushed=True)
	machine.AddCircuit(type="flip",name="flip", pushed=True)
	machine.AddCircuit(type="opSub",name="sub", pushed=True)
	machine.AddCircuit(type="SKLP",name="lowpass", fcut=1.1, pushed=True)
	
  	machine.Connect('vco.sin','ff1.clock')
  	machine.Connect('osc.sin','ff2.clock')
  	
  	machine.Connect('ff1.Q','and.in1','sub.in1')
  	machine.Connect('ff2.Q','and.in2','sub.in2')
  	machine.Connect('and.out','flip.signal')
  	machine.Connect('flip.tick','ff1.R','ff2.R')
  	machine.Connect('and.out','ff1.R','ff2.R')
  	machine.Connect('sub.out','lowpass.signal')
  	'''
	machine.Connect("osc.cos","pfd.ref")
	machine.Connect("vco.cos","pfd.vco")
	machine.Connect('pfd.df','frq.in1')
	machine.Connect('frq.out','vco.freq')
	
	out1 = machine.AddCircuit(type='output',name='output',file='test_dpfd.dat', dump=100)
	out1.Register('global.time', 'pfd.ref', 'pfd.vco', 'pfd.df', 'pfd.dbg')
	#out1.Register('global.time', 'vco.sin', 'osc.sin','and.out','flip.tick',
	#	'ff1.Q','ff2.Q','sub.out','lowpass.out')
	
	machine.Wait(0.05)
	
		
if __name__ == '__main__':
	main()


