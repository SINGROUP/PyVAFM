#!/usr/bin/env python
import sys
sys.path.append('/Users/johntracey/Desktop/pyvafm-master/src')



from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits

def main():

        
	machine = Machine(machine=None, name='machine', dt=0.01)
	scan = machine.AddCircuit(type='Scanner',name='scann', pushed=True)
	inter = machine.AddCircuit(type='i3Dlin',name='inter', components=3, pushed=True)

	inter.Configure(steps=[0.705,0.705,0.1], npoints=[8,8,171])
	inter.Configure(pbc=[True,True,False])
	#inter.Configure(ForceMultiplier=1e10)
	inter.ReadData('NaClforces.dat')

	machine.Connect("scann.x" , "inter.x")
	machine.Connect("scann.y" , "inter.y")
	machine.Connect("scann.z" , "inter.z")
	

    #Outputs
	out1 = machine.AddCircuit(type='output',name='output',file='interpolationtest.dat', dump=1)
	out1.Register('global.time', "scann.x","scann.y","scann.z",'inter.F1')

	#image output
	imager = machine.AddCircuit(type='output',name='image',file='NACLINTERTEST.dat', dump=0)
	imager.Register("scann.x", "scann.y", 'inter.F3')

	machine.Connect("scann.record", "image.record")
	

	
	'''
	scan.MoveTo(x=1,v=1)
	scan.Place(x=0,z=0.1)
	scan.MoveTo(x=1,v=1)
	scan.Place(x=0,z=0.2)
	scan.MoveTo(x=1,v=1)
	'''

	scan.Place(x=0, y=0, z=4)
	#this will print an empty line after each scanline
	scan.Recorder = imager
	scan.BlankLines = True 
	#not necessary, but it makes it easier for gnuplot
	
	#resolution of the image [# points per line, # lines]
	scan.Resolution = [512,512]
	scan.ImageArea(11.28,11.28) 
	
	#scan
	scan.ScanArea()



if __name__ == '__main__':
        main()
