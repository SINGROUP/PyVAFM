

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	
	#Add Circuits
	
	scanner = machine.AddCircuit(type='Scanner',name='scan', pushed=True )
	machine.AddCircuit(type='VDW', name='VDW', gamma=0.28658 ,hamaker=39.6e-20 ,radius=3.9487, offset=0 , pushed=True)

	machine.AddCircuit(type='VDWtorn', name='VDWtorn', A1=230325, A2=29640.6,A3=289318,A4=-5.19433e7,A5=2.27228e9,tipoffset=0)
	
	#debug output
	out1 = machine.AddCircuit(type='output',name='output',file='VDW.dat', dump=1)
	out1.Register("scan.z", "VDW.fz","VDWtorn.fz")
	

	machine.Connect("scan.z","VDW.ztip","VDWtorn.ztip")

	scanner.Place(x=0,y=0,z=0)
	#scanner.Move(x=0,y=0,z=0,v=1)
	machine.Wait(10)
if __name__ == '__main__':
	main()

