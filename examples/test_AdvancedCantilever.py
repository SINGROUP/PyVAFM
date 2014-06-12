#!/usr/bin/env python
from vafmcircuits import Machine
from customs_pll import *

def main():
	
	
	machine = Machine(name='machine', dt=0.02, pushed=True);
	f0 = 100.0
	
	#Add Circuits
	canti = machine.AddCircuit(type='AdvancedCantilever',name='canti', NumberOfModesV=2, NumberOfModesL=1 ,pushed=True)
	scanner = machine.AddCircuit(type='Scanner',name='scan', pushed=True )

	machine.AddCircuit(type='waver',name='wave', amp=10, freq=1, phi=1, offset=0, pushed=True)

	canti.AddMode(Vertical=True, k = 1, Q=100, M=1, f0 =1)
	canti.AddMode(Vertical=True, k = 1, Q=100, M=1, f0 =1)
	canti.AddMode(Vertical=False, k = 1, Q=100, M=1, f0 =1)
	canti.StartingPos(0,3,5)
	canti.CantileverReady()

	machine.Connect("scan.x","canti.Holderx")
	machine.Connect("scan.y","canti.Holdery")
	machine.Connect("scan.z","canti.Holderz")
#	machine.Connect("wave.cos","canti.ForceV")
#	machine.Connect("wave.cos","canti.ForceL")

	#debug output
	out1 = machine.AddCircuit(type='output',name='output',file='AdvCantilever.dat', dump=1)
	out1.Register("global.time","canti.zPos","canti.yPos","canti.xABS","canti.yABS","canti.zABS","canti.zV1","canti.zV2")
	

	scanner.Place(x=1,y=1,z=1)
	machine.Wait(15)

if __name__ == '__main__':
	main()


