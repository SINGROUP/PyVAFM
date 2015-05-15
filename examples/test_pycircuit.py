#!/usr/bin/env python

from vafmcircuits import Machine


def main():
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	
	#Add Circuits
	
	machine.AddCircuit(type='waver',name='wave', amp=1, freq=1, pushed=True )
  	machine.AddCircuit(type='myCirc',name='pytest', pushed=True )
	
	machine.Connect("wave.sin","pytest.in1")
	machine.Connect("wave.cos","pytest.in2")

	out1 = machine.AddCircuit(type='output',name='output',file='test_pycircuit.out', dump=1)
	out1.Register('global.time', 'wave.sin', 'pytest.out')
	
	machine.Wait(1)

if __name__ == '__main__':
	main()

