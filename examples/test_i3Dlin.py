#!/usr/bin/env python
from vafmcircuits import Machine

def main():

	machine = Machine(machine=None, name='machine', dt=0.01)
	scan = machine.AddCircuit(type='Scanner',name='scann', pushed=True)
	inter = machine.AddCircuit(type='i3Dlin',name='inter', components=1, pushed=True)

	inter.Configure(steps=[0.805714285714286,0.805714285714286,0.1], npoints=[8,8,171])
	inter.Configure(pbc=[True,True,False])
	inter.Configure(ForceMultiplier=1e10)
	inter.ReadData('NaClforces.dat')

	machine.Connect("scann.x" , "inter.x")
	machine.Connect("scann.y" , "inter.y")
	machine.Connect("scann.z" , "inter.z")
	
    #Outputs
	out1 = machine.AddCircuit(type='output',name='output',file='test_i3Dlin.out', dump=1)
	out1.Register('global.time', "scann.x","scann.y","scann.z",'inter.F1')

	#image output
	imager = machine.AddCircuit(type='output',name='image',file='test.dat', dump=0)
	imager.Register("scann.x", "scann.y", 'inter.F1')

	machine.Connect("scann.record", "image.record")
	
	scan.Place(x=0.805714285714286, y=0.805714285714286, z=4)

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
