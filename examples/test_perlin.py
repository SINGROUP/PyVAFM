#!/usr/bin/env python

from vafmcircuits import Machine


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	machine.AddCircuit(type='Perlin', name='noise', octaves=2, persist=0.5, amp=1, period=0.1, pushed=True)
	
	#debug output
	out1 = machine.AddCircuit(type='output',name='output',file='test_perlin.out', dump=1)
	out1.Register("global.time","noise.out")
	
	machine.Wait(1)

if __name__ == '__main__':
	main()


