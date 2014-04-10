
import vafmcircuits
from customs_pll import *
#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine



def main():
	
	
	machine = Machine(name='machine', dt=3e-8, pushed=True);
	f0 = 100000.0
	
	#Add Circuits
	canti = machine.AddCircuit(type='Cantilever',name='canti', startingz=0.5,
		Q=10000, k=167.0, f0=f0, pushed=True)

	machine.AddCircuit(type='delay', name='phi', DelayTime=0.5/f0, pushed=True)
	machine.AddCircuit(type='Machine', name='ampd', assembly=aAMPD, fcut=10000, pushed=True)
	machine.AddCircuit(type='PI', name='agc', Kp=1.1, Ki=80, set=1, pushed=True)



	#####################################################################################
	#dfpd setup

	machine.AddCircuit(type='waver',name='test', amp=1, freq=f0, pushed=True)

	machine.AddCircuit(type='waver',name='vco', amp=1, freq=f0, pushed=True)
	machine.AddCircuit(type="Machine",name='pfd', assembly=dPFD, gain=1000.0, fcut=1000, KI=-350,KP=-0.7	, pushed=True)
	machine.AddCircuit(type='opAdd',name='frq', in2=f0, pushed=True)	


	#####################################################################################



	machine.AddCircuit(type='opMul',name='exciter',pushed=True)
	
	#machine.AddCircuit(type='waver', name='wave', freq=100000.0, pushed=True)
	scanner = machine.AddCircuit(type='Scanner',name='scan', Process = machine, pushed=True)



	inter = machine.AddCircuit(type='i3Dlin',name='inter', components=3, pushed=True)
	inter.Configure(steps=[0.805714285714286,0.805714285714286,0.1], npoints=[8,8,171])
	inter.Configure(pbc=[True,True,False])
	inter.Configure(ForceMultiplier=1e10)
	inter.ReadData('NaClforces.dat')




	#Imaging output
	imager = machine.AddCircuit(type='output',name='image',file='test_dpfd.dat', dump=0)
	imager.Register("scan.x","scan.y","pfd.df")

	#out1 = machine.AddCircuit(type='output',name='output',file='debug_dpfd.dat', dump=1000)
	#out1.Register('scan.x','global.time', 'pfd.ref', 'pfd.vco', 'pfd.df', 'canti.zabs','exciter.out')


	#Debug output
	#out1 = machine.AddCircuit(type='output',name='output',file='Debug.dat', dump=1)
	#out1.Register('global.time', "scan.x", "scan.y", "scan.z", 'image.record',"canti.zabs")
	
    #feed x and y to interpolation
	machine.Connect("scan.x" , "inter.x")
	machine.Connect("scan.y" , "inter.y")

    #feed z to cantilever then the ztip of canti to interpolation
	machine.Connect("scan.z" , "canti.holderz")
	machine.Connect("canti.zabs" , "inter.z")

    #feed force to canti
	machine.Connect("inter.F3" , "canti.fz")
	

	
	machine.Connect('canti.ztip','ampd.signal')
	machine.Connect('ampd.amp','agc.signal')
	
	machine.Connect("ampd.norm","phi.signal")	



	#####################################################################################
	#dpfd connections
	machine.Connect("phi.out","pfd.ref")
	#machine.Connect("test.cos","pfd.ref")
	machine.Connect("vco.cos","pfd.vco")
	machine.Connect('pfd.df','frq.in1')
	machine.Connect('frq.out','vco.freq')
	
	#####################################################################################


	machine.Connect('agc.out','exciter.in1')


	#####################################################################################
	#Dpfd excitation
	machine.Connect('vco.cos','exciter.in2')
	machine.Connect('exciter.out','canti.exciter')

	#####################################################################################


	machine.Connect("scan.record","image.record")	
	


	#machine.SetInput(channel="output.record", value=0)

	scanner.Place(x=0.805714285714286,y=0.805714285714286,z=4.5)
	
	#scanner.Move(x=0,y=0,z=-0.5)	
	machine.Wait(0.5)
	'''
	machine.SetInput(channel="test.freq", value=f0+2)
	machine.Wait(0.5)
	print "WAITING DONE"
	'''

	#machine.SetInput(channel="output.record", value=1)	
	scanner.Recorder = imager
	scanner.BlankLines = True 
	#resolution of the image [# points per line, # lines]
	scanner.Resolution = [30,30]
	scanner.ImageArea(12,12)        
	#scan
	scanner.ScanArea()
	


if __name__ == '__main__':
	main()