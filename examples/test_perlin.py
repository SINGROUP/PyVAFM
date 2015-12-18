#!/usr/bin/env python

from vafmcircuits import Machine


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	machine.AddCircuit(type='Perlin', name='noise', octaves=16, persist=1, amp=0.005, period=0.1, pushed=True)
	
	#debug output
	out1 = machine.AddCircuit(type='output',name='output',file='test_perlin.out', dump=1)
	out1.Register("global.time","noise.out")
	
	machine.Wait(3)

if __name__ == '__main__':
	main()


