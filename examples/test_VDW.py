##!/usr/bin/env python
import subprocess
import sys
sys.path.append('/Users/johntracey/Desktop/pyvafm-master/src')

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	
	#Add Circuits
	
	scanner = machine.AddCircuit(type='Scanner',name='scan', pushed=True )
	machine.AddCircuit(type='VDW', name='VDW', gamma=0.28658 ,hamaker=39.6e-20 ,radius=3.9487, offset=0 , pushed=True)

	'''
	#xe-ar
	#dimer
	machine.AddCircuit(type='VDWtorn', name='Dimer',A1=-0.0166279, A2=0.22753, A3=-1819.29, A4=27055.6, A5=-106878., A6=31.8093, tipoffset=0, pushed=True)

	#Surface
	machine.AddCircuit(type='VDWtorn', name='Pyramid', A1=-1884.77, A2=619.586, A3=-1391.33, A4=22337., A5=-93389.1, A6=17.5403,tipoffset=0, pushed=True)
 
	#Pyramid
	machine.AddCircuit(type='VDWtorn', name='Surface', A1=-462.061, A2=99.2976, A3=212.33, A4=-682.216, A5=646.31, A6=-7.59327,tipoffset=0, pushed=True)
	

	'''
	#xe-Kr
	#dimer
	machine.AddCircuit(type='VDWtorn', name='Dimer',A1=0.263191, A2=0.527478, A3=-1259.79, A4=23749.8, A5=-88463.2, A6=-4.00773, tipoffset=0, pushed=True)

	#Surface
	machine.AddCircuit(type='VDWtorn', name='Pyramid', A1=-1925.32, A2=635.529, A3=-1160.23, A4=22763.2, A5=-101664., A6=1.99542,tipoffset=0, pushed=True)
 
	#Pyramid
	machine.AddCircuit(type='VDWtorn', name='Surface', A1=-891.534, A2=416.779, A3=1558.35, A4=-8353.84, A5=15269.4, A6=-84.7053,tipoffset=0, pushed=True)
		

	'''
	#xe-xe
	#dimer
	machine.AddCircuit(type='VDWtorn', name='Dimer',A1=0.624987, A2=0.42742, A3=1686.2, A4=-12092.2, A5=115496., A6=-115.753, tipoffset=0, pushed=True)

	#Surface
	machine.AddCircuit(type='VDWtorn', name='Pyramid',A1=-1987.09, A2=658.103, A3=-587.187, A4=21188.8, A5=-107670., A6=-26.6053,tipoffset=0, pushed=True)
 
	#Pyramid
	machine.AddCircuit(type='VDWtorn', name='Surface', A1=-883.96, A2=412.92, A3=1705.83, A4=-9119.11, A5=16490.2, A6=-87.6929,tipoffset=0, pushed=True)
	'''


	#debug output
	out1 = machine.AddCircuit(type='output',name='output',file='VDW.dat', dump=1)
	out1.Register("scan.z","global.time","VDW.fz","Dimer.fz","Surface.fz","Pyramid.fz")
	

	machine.Connect("scan.z","VDW.ztip","Dimer.ztip","Surface.ztip","Pyramid.ztip")


	scanner.Place(x=0,y=0,z=15)
	scanner.MoveTo(x=0,y=0,z=4,v=1)
	#machine.Wait(10)
if __name__ == '__main__':
	main()

