#!/usr/bin/env python
import subprocess
import sys
sys.path.append('/Users/johntracey/Desktop/pyvafm-master/src')

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
from customs_pll import *


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	f0 = 100.0
	
	#Add Circuits
	canti = machine.AddCircuit(type='AdvancedCantilever',name='canti',NumberOfModesV=2,NumberOfModesL=0, pushed=True)

	canti.AddK(1.1,2.2)
	canti.AddQ(1.2,2.3)
	canti.AddM(1.3,2.4)
	canti.Addf0(1.4,2.5)
	canti.StartingPos(1.5,2.6,2.7)

	#debug output
	out1 = machine.AddCircuit(type='output',name='output',file='AdvCantilever.dat', dump=1000)
	out1.Register("global.time","canti.zPos")
	
	machine.Wait(0.02)

if __name__ == '__main__':
	main()


