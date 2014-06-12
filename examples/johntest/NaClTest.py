#!/usr/bin/env python
from vafmcircuits import Machine
from customs_pll import *


'''
UNITS:
	distance	= nm
	force		= nN
	time		= s
'''

def main():

	machine = Machine(machine=None, name='machine', dt=5.0e-8)
#	canti = machine.AddCircuit(type='Cantilever',name='canti', 
#		Q=20000, k=26.4, f0=150000, startingz=1, pushed=True)
	
	A0 = 0.2

	canti = machine.AddCircuit(type='Cantilever',name='canti', startingz=0.5*A0,
		Q=10000, k=167.0, f0=150000, pushed=True)

	#machine.AddCircuit(type='waver',name='wave',freq=150000,amp=1)

	#Amplitude stuff: I changed the settings a bit so the noise is less than 1 pm
	machine.AddCircuit(type="Machine",name='amp', fcut=5000, assembly=aAMPD, 
		pushed=True)
	machine.AddCircuit(type='PI', name='agc', Kp=1.0, Ki=100, set=A0, pushed=True)
	machine.AddCircuit(type="limiter",name='agclim', min=0,max=10, pushed=True)
	
	machine.AddCircuit(type="Machine",name='pll', fcut=1000, assembly=aPLL, 
		filters=[10000,5000,2000], gain=600.0, f0=150000, Kp=0.5, Ki=700, 
		pushed=True)
	
	machine.AddCircuit(type='opMul',name='pllinv',in2=-1, pushed=True)
	machine.AddCircuit(type='opMul',name='exc', pushed=True)

	scanner = machine.AddCircuit(type='Scanner',name='scan', Process = machine, pushed=True)


	inter = machine.AddCircuit(type='i3Dlin',name='inter', components=3, pushed=True)
	inter.Configure(steps=[0.0705,0.0705,0.01], npoints=[8,8,201]) # I converted it back to nN
	inter.Configure(pbc=[True,True,False])
	inter.Configure(ForceMultiplier=1e9) # I converted it back to nN
	inter.ReadData('NaClforces.dat')

	
    #Outputs
	out1 = machine.AddCircuit(type='output',name='output',file='testafm.out', dump=2)
	out1.Register('global.time', 'canti.zabs','amp.norm','pll.cos','pll.sin','exc.in2')
	#out1.Register('global.time', 'wave.cos','pll.cos','pll.sin','exc.in2')
	out1.Stop()

	out2 = machine.AddCircuit(type='output',name='output2',file='testafm2.out', dump=100000)
	out2.Register('global.time', 'amp.amp','agc.out','pll.df',"canti.fz",'scan.z')#always monitor the amplitude
	

	#Imaging output
	imager = machine.AddCircuit(type='output',name='image',file='NaCl.dat', dump=0)
	imager.Register("scan.x","scan.y","pll.df","amp.amp")


    #feed x and y to interpolation
	machine.Connect("scan.x" , "inter.x")
	machine.Connect("scan.y" , "inter.y")
	machine.Connect("scan.z" , "canti.holderz")
	machine.Connect("canti.zabs" , "inter.z")

	#Force
	machine.Connect("inter.F3" , "canti.fz")	
	
	machine.Connect('canti.ztip','amp.signal')
	machine.Connect('amp.amp','agc.signal')
	machine.Connect('amp.norm','pll.signal1')
	#machine.Connect('wave.cos','pll.signal1')
	machine.Connect('pll.cos','pll.signal2')
	
	machine.Connect('agc.out','agclim.signal')
	machine.Connect('agclim.out','exc.in1')
	machine.Connect('pll.cos','pllinv.in1')
	machine.Connect('pllinv.out','exc.in2')
	
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
	
	holderstartz = 3 #start at 3nm high
	
	out2.Stop()
	scanner.Place(x=0,y=0,z=holderstartz)
	machine.Wait(0.1) # prerelaxation we do not want to see in out2
	out2.Start()
	machine.Wait(0.5) #these does not give any visual feedback.... we dont know if the program crashed!
	
	scanner.FastSpeed = 10 # approach faster
	
	#amp is 1nm, to image at a min approach distance of 5 angs, 
	#we need to approach by 15nm-amp-0.5nm
	scanner.Move(x=0,y=0,z=-(holderstartz-A0-0.5))
	machine.Wait(1)	

		
	machine.SetInput(channel="output.record", value=1)	
	scanner.Recorder = imager
	scanner.BlankLines = True 
	#resolution of the image [# points per line, # lines]
	scanner.Resolution = [512,512]
	scanner.ImageArea(1.128,1.128)
	scanner.FastSpeed = 10
	scanner.SlowSpeed = 10
	#scan
	scanner.ScanArea()
	

if __name__ == '__main__':
        main()

