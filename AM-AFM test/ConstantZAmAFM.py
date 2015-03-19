#!/usr/bin/env python
from vafmcircuits import Machine
from customs_pll import *

#A = 9.75
#A = 9.82
A=0.98
machine = Machine(machine=None, name='machine', dt=5.0e-8)


scanner = machine.AddCircuit(type='Scanner',name='scan', Process = machine, pushed=True)


canti = machine.AddCircuit(type='Cantilever',name='canti', startingz=0.5,
	Q=4, k=4.0, f0=150000, pushed=True)



#+ve force grad gives a -ve freq shift moving the canti further from res and hence reducing amp...
#10
machine.AddCircuit(type='waver',name='wave',freq=150000+1000 ,amp=1)


machine.AddCircuit(type="Machine",name='amp', fcut=1000, assembly=aAMPD, pushed=True)


inter = machine.AddCircuit(type='i3Dlin',name='inter', components=3, pushed=True)
inter.Configure(steps=[0.705,0.705,0.1], npoints=[8,8,171])
inter.Configure(pbc=[True,True,False])
inter.Configure(ForceMultiplier=1e10)
inter.ReadData('NaClforces.dat')

    #Outputs
out1 = machine.AddCircuit(type='output',name='output',file='testafm.out', dump=50000)
out1.Register('global.time','scan.x' ,'canti.zabs','amp.amp',"inter.F3",'canti.holderz')
out1.Stop()

#Imaging output
imager = machine.AddCircuit(type='output',name='image',file='ConstantNaCl.dat', dump=0)
imager.Register("scan.x","scan.y",'amp.amp')

machine.Connect("scan.x" , "inter.x")
machine.Connect("scan.y" , "inter.y")
machine.Connect("canti.zabs" , "inter.z")
#machine.Connect("scan.z" , "inter.z")



machine.Connect("inter.F3" , "canti.fz")


machine.Connect('canti.ztip','amp.signal')
machine.Connect('wave.sin','canti.exciter')

machine.Connect("scan.z" , "canti.holderz")

machine.Connect("scan.record","image.record")

#out1.Start()

scanner.Place(x=0,y=0,z=5)
machine.Wait(1)
#scanner.Move(x=10)


#machine.SetInput(channel="output.record", value=1)	
scanner.Recorder = imager
scanner.BlankLines = True 
#resolution of the image [# points per line, # lines]
scanner.Resolution = [64,64]
scanner.ImageArea(11.28,11.28)        
#scan
scanner.ScanArea()
