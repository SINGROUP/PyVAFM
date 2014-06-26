#!/usr/bin/env python
from vafmcircuits import Machine

def main():

	machine = Machine(machine=None, name='machine', dt=0.01)
	
	machine.AddCircuit(type='STM',name='STM', pushed=True)
	
	inter = machine.AddCircuit(type='i4Dlin',name='inter', components=1, pushed=True)
	inter.BiasStep=0.5
	inter.StartingV=1
	inter.ReadVASPData("parchg.1.0","parchg.1.5","parchg.2.0")

	scanner = machine.AddCircuit(type='Scanner',name='scan', pushed=True )



	out1 = machine.AddCircuit(type='output',name='output',file='test4d.dat', dump=1)
	out1.Register('scan.x', 'scan.y','scan.z','STM.Current')	

	machine.Connect("scan.x","inter.x")
	machine.Connect("scan.y","inter.y")
	machine.Connect("scan.z","inter.z")
	machine.Connect("inter.F1","STM.Density")


	machine.circuits['inter'].I['V'].Set(1)
	scanner.Place(x=0,y=0,z=0)

#	machine.Wait(0.01)

if __name__ == '__main__':
        main()
