

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	
	#Add Circuits
	
	scanner = machine.AddCircuit(type='Scanner',name='scan', pushed=True )
	machine.AddCircuit(type='VDW', name='VDW', gamma=0.28658 ,hamaker=39.6e-20 ,radius=3.9487, offset=0 , pushed=True)

	machine.AddCircuit(type='VDWtorn', name='VDWtorn', A1=1, A2=1,A3=1,A4=1,A5=1,tipoffset=0)
	
	#debug output
	out1 = machine.AddCircuit(type='output',name='output',file='VDW.dat', dump=1)
	out1.Register("scan.z", "VDW.fz","VDWtorn.fz")
	

	machine.Connect("scan.z","VDW.ztip","VDWtorn.ztip")

	scanner.Place(x=0,y=0,z=1)
	scanner.Move(x=0,y=0,z=10,v=1)

if __name__ == '__main__':
	main()

