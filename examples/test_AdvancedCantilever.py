#!/usr/bin/env python
import subprocess
import sys
sys.path.append('/Users/johntracey/Desktop/pyvafm-master/src')

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
from customs_pll import *


def main():
	
	
	machine = Machine(name='machine', dt=0.02, pushed=True);
	f0 = 100.0
	
	#Add Circuits
	canti = machine.AddCircuit(type='AdvancedCantilever',name='canti',NumberOfModesV=0,NumberOfModesL=2, pushed=True)
	scanner = machine.AddCircuit(type='Scanner',name='scan', pushed=True )



	canti.AddK(1,1)
	canti.AddQ(1000000,1000000)
	canti.Addf0(1,1)
	canti.AddM(1,1)

	canti.StartingPos(0,3,5)


	machine.Connect("scan.x","canti.Holderx")
	machine.Connect("scan.y","canti.Holdery")
	machine.Connect("scan.z","canti.Holderz")

	#debug output
	out1 = machine.AddCircuit(type='output',name='output',file='AdvCantilever.dat', dump=1)
	out1.Register("global.time","canti.zPos","canti.yPos","canti.xABS","canti.yABS","canti.zABS","canti.yL1","canti.yL2")
	

	scanner.Place(x=1,y=1,z=1)
	machine.Wait(10)

if __name__ == '__main__':
	main()


