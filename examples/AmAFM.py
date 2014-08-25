#!/usr/bin/env python
from vafmcircuits import Machine
from customs_pll import *


def main():

	machine = Machine(machine=None, name='machine', dt=5.0e-8)
#	canti = machine.AddCircuit(type='Cantilever',name='canti', 
#		Q=20000, k=26.5, f0=150000, startingz=1, pushed=True)


	canti = machine.AddCircuit(type='Cantilever',name='canti', startingz=0.5,
		Q=10000, k=167.0, f0=150000, pushed=True)

	machine.AddCircuit(type='waver',name='wave',freq=150000-100,amp=1)

	machine.AddCircuit(type="Machine",name='amp', fcut=10000, assembly=aAMPD, 
		pushed=True)
	
#	machine.AddCircuit(type="PI",name='agc', Ki=2.1, Kp=0.1, set=0.1, pushed=True)
	machine.AddCircuit(type='PI', name='agc', Kp=1.1, Ki=800, set=1, pushed=True)
	machine.AddCircuit(type="limiter",name='agclim', min=0,max=10, pushed=True)
	
	machine.AddCircuit(type="Machine",name='pll', fcut=1000, assembly=aPLL, 
		filters=[10000,5000,2000], gain=600.0, f0=150000, Kp=0.5, Ki=700, 
		pushed=True)
	
	machine.AddCircuit(type='opMul',name='pllinv',in2=-1, pushed=True)
	machine.AddCircuit(type='opMul',name='exc', pushed=True)

	scanner = machine.AddCircuit(type='Scanner',name='scan', Process = machine, pushed=True)


	inter = machine.AddCircuit(type='i3Dlin',name='inter', components=3, pushed=True)
	inter.Configure(steps=[0.705,0.705,0.1], npoints=[8,8,171])
	inter.Configure(pbc=[True,True,False])
	inter.Configure(ForceMultiplier=1e10)
	inter.ReadData('NaClforces.dat')




	
    #Outputs
	out1 = machine.AddCircuit(type='output',name='output',file='testafm.out', dump=10000)
	out1.Register('global.time', 'canti.zabs','amp.norm','exc.in2')
	#out1.Register('global.time', 'wave.cos','pll.cos','pll.sin','exc.in2')
	out1.Stop()

	out2 = machine.AddCircuit(type='output',name='output2',file='testafm2.out', dump=1000)
	out2.Register('global.time', 'canti.ztip','agc.out',"canti.fz","amp.amp")
	out2.Stop()

	#Imaging output
	imager = machine.AddCircuit(type='output',name='image',file='NaCl.dat', dump=0)
	imager.Register("scan.x","scan.y",'agc.out')	


    #feed x and y to interpolation
	machine.Connect("scan.x" , "inter.x")
	machine.Connect("scan.y" , "inter.y")
	machine.Connect("scan.z" , "canti.holderz")
	machine.Connect("canti.zabs" , "inter.z")

	#Force
	machine.Connect("inter.F3" , "canti.fz")	
	
	machine.Connect('canti.ztip','amp.signal')
	machine.Connect('amp.amp','agc.signal')
	#machine.Connect('amp.norm','pll.signal1')
	#machine.Connect('wave.cos','pll.signal1')
	#machine.Connect('pll.cos','pll.signal2')
	
	machine.Connect('agc.out','agclim.signal')
	machine.Connect('agclim.out','exc.in1')
#	machine.Connect('pll.cos','pllinv.in1')
#	machine.Connect('pllinv.out','exc.in2')
	machine.Connect('wave.sin','exc.in2')


	
	machine.Connect('exc.out','canti.exciter')

	machine.Connect("scan.record","image.record")	
	


	

	'''
	machine.Wait(0.01)
	out1.Start()
	machine.Wait(0.001)
	out1.Stop()
	machine.Wait(0.05)
	out1.Start()
	machine.Wait(0.001)
	'''
	#plot testafm.out 1:3 (canti) 1:4 (pll reference) 1:6 (the exciter)
	#u should see 3 distinct waves, canti peaks are in the middle between the other 2

	scanner.Place(x=0,y=0,z=15)
	machine.Wait(0.5)	

	scanner.Move(x=0,y=0,z=-11)
	machine.Wait(1)	


	
		
	#machine.SetInput(channel="output.record", value=1)	
	scanner.Recorder = imager
	scanner.BlankLines = True 
	#resolution of the image [# points per line, # lines]
	scanner.Resolution = [20,1]
	scanner.ImageArea(11.28,11.28)        
	#scan
	scanner.ScanArea()
	

if __name__ == '__main__':
        main()

