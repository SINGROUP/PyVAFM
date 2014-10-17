#!/usr/bin/env python
from vafmcircuits import Machine

machine = Machine(machine=None, name='machine', dt=0.01)

#machine.AddCircuit(type='CoordTransform',name='CT', LatticeVectorX=[15.562592,0.0,0.0], LatticeVectorY=[-7.781296,13.4776,0.0], LatticeVectorZ=[15.562592,-8.985067,25.413607] ,pushed=True)


scan = machine.AddCircuit(type='Scanner',name='scann')
#inter = machine.AddCircuit(type='i3Dlin',name='inter', components=1)

'''
inter.Configure(steps=[0.072049037037, 0.0748755555556, 0.075635735119], npoints=[216,180,332])
inter.Configure(pbc=[True,True,False])
inter.ReadData('TestCeo2.dat')
'''

inter = machine.AddCircuit(type='i3Dlin',name='inter', components=3, pushed=True)
inter.Configure(steps=[0.705,0.705,0.1], npoints=[8,8,201])
inter.Configure(pbc=[True,True,False])
inter.Configure(ForceMultiplier=1e10)
inter.ReadData('NaClforces.dat')


machine.Connect("scann.x" , "inter.x")
machine.Connect("scann.y" , "inter.y")
machine.Connect("scann.z" , "inter.z")

#machine.Connect("CT.xprime","inter.x")
#machine.Connect("CT.yprime","inter.y")
#machine.Connect("CT.zprime","inter.z")




dist = 0


#image output
imager = machine.AddCircuit(type='output',name='image',file='test.dat', dump=0)
imager.Register("scann.x", "scann.y", 'inter.F3')

machine.Connect("scann.record", "image.record")

#machine.Wait(0.01)
	
#this will print an empty line after each scanline
scan.Recorder = imager
scan.BlankLines = True 
scan.Resolution = [64,64]
scan.ImageArea(12,12) 

scan.Place(x=0, y=0, z=10)
	
#scan
scan.ScanArea()
dist += 1

