#!/usr/bin/env python
from vafmcircuits import Machine

def main():

	machine = Machine(machine=None, name='machine', dt=0.01)

	machine.AddCircuit(type='CoordTransform',name='CT', LatticeVectorX=[15.562592,0.0,0.0], LatticeVectorY=[-7.781296,13.4776,0.0], LatticeVectorZ=[15.562592,-8.985067,25.413607] ,pushed=True)
	

	scan = machine.AddCircuit(type='Scanner',name='scann')
	inter = machine.AddCircuit(type='i3Dlin',name='inter', components=1)

	inter.Configure(steps=[0.1, 0.1, 0.1], npoints=[155,155,307])
	inter.Configure(pbc=[True,True,False])
	inter.ReadData('Cerium.dat')

	machine.Connect("scann.x" , "inter.x")
	machine.Connect("scann.y" , "inter.y")
	machine.Connect("scann.z" , "inter.z")

	#machine.Connect("CT.xprime","inter.x")
	#machine.Connect("CT.yprime","inter.y")
	#machine.Connect("CT.zprime","inter.z")


	#image output
	imager = machine.AddCircuit(type='output',name='image',file='CeriumFF.dat', dump=0)
	imager.Register("scann.x", "scann.y", 'inter.F1',)

	machine.Connect("scann.record", "image.record")

	scan.Place(x=0, y=0, z=13)
	#machine.Wait(0.01)
	
	#this will print an empty line after each scanline
	scan.Recorder = imager
	scan.BlankLines = True 
	#not necessary, but it makes it easier for gnuplot
		
	#resolution of the image [# points per line, # lines]
	scan.Resolution = [256,256]
	scan.ImageArea(16,16) 
		
	#scan
	scan.ScanArea()


if __name__ == '__main__':
        main()
