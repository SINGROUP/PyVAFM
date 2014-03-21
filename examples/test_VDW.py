#!/usr/bin/env python
import sys
sys.path.append('/Users/johntracey/Desktop/pyvafm-master/src')


from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	
	#Add Circuits
	
	scanner = machine.AddCircuit(type='Scanner',name='scan', pushed=True )
	machine.AddCircuit(type='VDW', name='VDW', alpha=0.28658 ,hamaker=39.6e-20 ,radius=3.9487, offset=0 , pushed=True)

	
	
	#debug output
	out1 = machine.AddCircuit(type='output',name='output',file='VDW.dat', dump=1)
	out1.Register("scan.z", "VDW.fz")
	

	machine.Connect("scan.z","VDW.ztip")

	scanner.Place(x=0,y=0,z=10)
	scanner.Move(x=0,y=0,z=10.1,v=1)

if __name__ == '__main__':
	main()

