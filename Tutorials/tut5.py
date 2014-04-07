import vafmcircuits
from customs_pll import *
from vafmbase import ChannelType
from vafmcircuits import Machine


machine = Machine(name='machine', dt=5e-8, pushed=True);
f0 = 100000.0
	
canti = machine.AddCircuit(type='Cantilever',name='canti', startingz=1, Q=10000, k=167.0, f0=f0, pushed=True)

machine.AddCircuit(type='delay', name='phi', DelayTime=0.5/f0, pushed=True)
machine.AddCircuit(type='Machine', name='ampd', assembly=aAMPD, fcut=10000, pushed=True)
machine.AddCircuit(type='PI', name='agc', Kp=1.1, Ki=800, set=2, pushed=True)

machine.AddCircuit(type='Machine',name='pll',assembly=aPLL,filters=[10000,5000,2000],gain=500.0, f0=f0, Kp=0.5, Ki=800, pushed=True)
machine.AddCircuit(type='opMul',name='exciter',pushed=True)
	

scanner = machine.AddCircuit(type='Scanner',name='scan', Process = machine, pushed=True)


inter = machine.AddCircuit(type='i3Dlin',name='inter', components=3, pushed=True)
inter.Configure(steps=[0.805,0.805,0.1], npoints=[8,8,171])
inter.Configure(pbc=[True,True,False])
inter.Configure(ForceMultiplier=1e10)
inter.ReadData('NaClforces.dat')


imager = machine.AddCircuit(type='output',name='image',file='tut5.dat', dump=0)
imager.Register("scan.x","scan.y","pll.df")


machine.Connect("scan.x" , "inter.x")
machine.Connect("scan.y" , "inter.y")

machine.Connect("scan.z" , "canti.holderz")
machine.Connect("canti.zabs" , "inter.z")


machine.Connect("inter.F3" , "canti.fz")
	

machine.Connect('canti.ztip','ampd.signal')
machine.Connect('ampd.amp','agc.signal')
	
machine.Connect("ampd.norm","phi.signal")	
machine.Connect("phi.out","pll.signal1")
machine.Connect("pll.cos","pll.signal2")
	
machine.Connect('agc.out','exciter.in1')
machine.Connect('pll.cos','exciter.in2')
machine.Connect('exciter.out','canti.exciter')


machine.Connect("scan.record","image.record")	
	



scanner.Place(x=1,y=1,z=5.5)
	
scanner.Move(x=0,y=0,z=-0.5)	
machine.Wait(0.02)


scanner.Recorder = imager
scanner.BlankLines = True 
scanner.Resolution = [24,24]
scanner.ImageArea(16,16)        
scanner.ScanArea()