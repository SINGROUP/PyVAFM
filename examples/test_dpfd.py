#!/usr/bin/env python

from vafmcircuits import Machine
from customs_pll import *


def main():
	
	f0=1.0e5
	
	machine = Machine(name='machine', dt=1.0e-8, pushed=True);
	
	machine.AddCircuit(type='waver',name='osc', amp=1, freq=f0+1.3, pushed=True)
	machine.AddCircuit(type='waver',name='vco', amp=1, freq=f0, pushed=True)
	machine.AddCircuit(type="Machine",name='pfd', assembly=dPFD, gain=1000.0, fcut=500, 
		KI=1.0,KP=0.30, pushed=True)
	
	machine.AddCircuit(type='opAdd',name='frq', in2=f0, pushed=True)
	
	machine.Connect("osc.cos","pfd.ref")
	machine.Connect("vco.cos","pfd.vco")
	machine.Connect('pfd.df','frq.in1')
	machine.Connect('frq.out','vco.freq')
	
	out1 = machine.AddCircuit(type='output',name='output',file='test_dpfd.out', dump=100)
	out1.Register('global.time', 'pfd.ref', 'pfd.vco', 'pfd.df')
	
	machine.Wait(0.1)


if __name__ == '__main__':
	main()

