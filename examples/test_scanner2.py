#!/usr/bin/env python

from vafmcircuits import Machine


def main():
	
	
	machine = Machine(name='machine', dt=1e-3, pushed=True);
	
	#Add Circuits
	scanner = machine.AddCircuit(type='Scanner',name='scan', pushed=True )

	
	#debug output
	out1 = machine.AddCircuit(type='output',name='output',file='test_scanner.out', dump=0)
	out1.Register('global.time', "scan.x", "scan.y", "scan.z")

	#machine.Connect("scan.record","output.record")	

	
	#scanner.Place(x=1,y=0,z=0)
	#scanner.Move(x=1,y=0,z=0,v=1)
	#machine.Wait(1)
	#scanner.MoveTo(x=3,y=0,z=0,v=1)
	#machine.Wait(1)
	scanner.MoveRecord(x=2,y=0,z=0,v=1,points=10)

	machine.Wait(1)
if __name__ == '__main__':
	main()

