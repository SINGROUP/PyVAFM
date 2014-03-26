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
	canti = machine.AddCircuit(type='AdvancedCantilever',name='canti',NumberOfModesV=0,NumberOfModesL=1, pushed=True)

	canti.AddK(1)
	canti.AddQ(10)
	canti.Addf0(1)
	canti.AddM(1)

	canti.StartingPos(0,0,1)

	#debug output
	out1 = machine.AddCircuit(type='output',name='output',file='AdvCantilever.dat', dump=1)
	out1.Register("global.time","canti.yPos")
	
	machine.Wait(10)

if __name__ == '__main__':
	main()


