#!/usr/bin/env python

from vafmcircuits import Machine
from customs_pll import *

def main():
	
	machine = Machine(name='machine', dt=1.0e-9, pushed=True);
	f0 = 100000.0
	
	#Add Circuits
	canti = machine.AddCircuit(type='Cantilever',name='canti', startingz=0.5,
		Q=10000, k=167.0, f0=f0, pushed=True)

	machine.AddCircuit(type='delay', name='phi', DelayTime=0.5/f0, pushed=True)
	machine.AddCircuit(type='Machine', name='ampd', assembly=aAMPD, fcut=10000, pushed=True)
	machine.AddCircuit(type='PI', name='agc', Kp=1.1, Ki=800, set=1, pushed=True)

	machine.AddCircuit(type='Machine',name='pll',assembly=aPLL,filters=[10000,5000,2000],
		gain=500.0, f0=f0, Kp=0.5, Ki=800, pushed=True)
	machine.AddCircuit(type='opMul',name='exciter',pushed=True)
	
	#machine.AddCircuit(type='waver', name='wave', freq=100000.0, pushed=True)
	
	machine.Connect('canti.ztip','ampd.signal')
	machine.Connect('ampd.amp','agc.signal')
	
	machine.Connect("ampd.norm","phi.signal")
	machine.Connect("phi.out","pll.signal1")
	machine.Connect("pll.cos","pll.signal2")
	
	machine.Connect('agc.out','exciter.in1')
	machine.Connect('pll.cos','exciter.in2')
	machine.Connect('exciter.out','canti.exciter')
	
	#debug output
	out1 = machine.AddCircuit(type='output',name='output',file='test_cantilever.log', dump=1000)
	out1.Register("global.time","ampd.amp","pll.df")
	
	machine.Wait(0.02)

if __name__ == '__main__':
	main()


