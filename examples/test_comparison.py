#!/usr/bin/env python

from vafmcircuits import Machine


def main():
	
	#main machine
	machine = Machine(name='machine', dt=0.0005, pushed=True);
	
	# wave generator
	machine.AddCircuit(type='waver',name='wave', amp=1, freq=2, pushed=True )
	
	machine.AddCircuit(type='Equal', name='eq', pushed=True)
	machine.AddCircuit(type='LessOrEqual', name='leq', pushed=True)
	machine.AddCircuit(type='GreaterOrEqual', name='geq', pushed=True)
	
	#connect oscillator to the filters
	machine.Connect("wave.cos","eq.in1","leq.in1","geq.in1")
	machine.Connect("wave.sin","eq.in2","leq.in2","geq.in2")
	
	#output to file
	out1 = machine.AddCircuit(type='output',name='output',file='test_comparison.out', dump=1)
	out1.Register('global.time','wave.cos','wave.sin','eq.out','leq.out','geq.out')
	
	machine.Wait(1)
	

if __name__ == '__main__':
	main()

