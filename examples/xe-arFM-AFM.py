
import vafmcircuits
from customs_pll import *
#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine



def main():
	
	
	machine = Machine(name='machine', dt=1e-7, pushed=True);
	f0=23065
	#Angstrom
	Az=0.387

	#Add Circuits

	scanner = machine.AddCircuit(type='Scanner',name='scan', Process = machine, pushed=True)

	#k=eV/ang^2
	canti = machine.AddCircuit(type='Cantilever',name='canti', startingz=Az,
		Q=42497, k=112.32, f0=f0, pushed=True)

	machine.AddCircuit(type='delay', name='phi', DelayTime=0.5/f0, pushed=True)
	machine.AddCircuit(type='Machine', name='ampd', assembly=aAMPD, fcut=500, pushed=True)
	machine.AddCircuit(type='PI', name='agc', Kp=4, Ki=400, set=Az, pushed=True)

 	#machine.AddCircuit(type='limiter', name='Forcelim', max=0.5, min=-0.5)

	#####################################################################################
	#dfpd setup

	machine.AddCircuit(type='waver',name='test', amp=1, freq=f0, pushed=True)
	machine.AddCircuit(type='waver',name='vco', amp=1, freq=f0, pushed=True)
	machine.AddCircuit(type="Machine",name='pfd', assembly=dPFD, gain=600.0, fcut=500, KI=-300,KP=-0.3	, pushed=True)
	machine.AddCircuit(type='opAdd',name='frq', in2=f0, pushed=True)	


	#####################################################################################



	machine.AddCircuit(type='opMul',name='exciter',pushed=True)
	




	machine.AddCircuit(type='VDWtorn', name='VDWtorn', A1=230325, A2=29640.6,A3=289318,A4=-5.19433e7,A5=2.27228e9,tipoffset=0, pushed=True)


	#Imaging output
	imager = machine.AddCircuit(type='output',name='image',file='xe-ar-df.dat', dump=0)
	imager.Register("scan.z","pfd.df")

	#debug output
	output = machine.AddCircuit(type='output',name='outputer',file='debug.dat', dump=1000)
	output.Register("global.time","scan.z","pfd.df","canti.zabs","canti.ztip","canti.fz","ampd.amp","agc.out")



	#Give ztip to van der walls
	machine.Connect('canti.ztip','ampd.signal')
	machine.Connect('canti.zabs','VDWtorn.ztip')


    #feed z to cantilever then the ztip of canti to interpolation
	machine.Connect("scan.z" , "canti.holderz")

    #feed force to canti
		

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
	#machine.Connect("VDWtorn.fz" , "Forcelim.signal")
	machine.Connect("VDWtorn.fz" , "canti.fz")

	#####################################################################################
	#Dpfd excitation

	machine.Connect('vco.cos','exciter.in2')
	machine.Connect('exciter.out','canti.exciter')

	#####################################################################################


	machine.Connect("scan.record","image.record")	
	




	
	scanner.Place(x=0,y=0,z=50)

	machine.Wait(1)

	scanner.MoveRecord(x=0,y=0,z=10,v=10,points=200)


if __name__ == '__main__':
	main()