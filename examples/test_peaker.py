#!/usr/bin/env python

from vafmcircuits import Machine


def main():
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	#Add Circuits
  	machine.AddCircuit(type='waver',name='osc', amp=0.2, freq=1.3, pushed=True )
	machine.AddCircuit(type='peaker', name='pkd', up=True, pushed=True)
	
	machine.Connect("osc.sin","pkd.signal")

	out1 = machine.AddCircuit(type='output',name='output',file='test_peaker.out', dump=1)
	out1.Register('global.time', "osc.sin","pkd.tick","pkd.peak","pkd.delay")
	
	machine.Wait(5)
	

if __name__ == '__main__':
	main()

