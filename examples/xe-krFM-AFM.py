#!/usr/bin/env python
from vafmcircuits import Machine
from customs_pll import *


def main():

	machine = Machine(machine=None, name='machine', dt=5e-8)

	f0=23065
	#Angstrom
	Az=0.387

	scanner = machine.AddCircuit(type='Scanner',name='scan', Process = machine, pushed=True)	
	
	canti = machine.AddCircuit(type='Cantilever',name='canti', 
		Q=42497, k=112.32, f0=f0, startingz=Az, pushed=True)

	machine.AddCircuit(type='waver',name='wave',freq=f0,amp=1)

	machine.AddCircuit(type="Machine",name='amp', fcut=500, assembly=aAMPD, 
		pushed=True)
	
	machine.AddCircuit(type="PI",name='agc', Ki=2.1, Kp=0.1, set=Az, pushed=True)
	machine.AddCircuit(type="limiter",name='agclim', min=0,max=10, pushed=True)
	
	machine.AddCircuit(type="Machine",name='pll', assembly=dPFD, gain=1000.0, fcut=500, KI=3,KP=0.5, f0=f0	, pushed=True)
	
	machine.AddCircuit(type='opMul',name='pllinv',in2=-1, pushed=True)
	machine.AddCircuit(type='opMul',name='exc', pushed=True)

	###################################################################
	#Force Setup
	#xe-Kr
	#dimer
	machine.AddCircuit(type='VDWtorn', name='Dimer',A1=0.263191, A2=0.527478, A3=-1259.79, A4=23749.8, A5=-88463.2, A6=-4.00773, tipoffset=0, pushed=True)

	#Surface
	machine.AddCircuit(type='VDWtorn', name='Pyramid', A1=-1925.32, A2=635.529, A3=-1160.23, A4=22763.2, A5=-101664., A6=1.99542,tipoffset=0, pushed=True)
 
	#Pyramid
	machine.AddCircuit(type='VDWtorn', name='Surface', A1=-891.534, A2=416.779, A3=1558.35, A4=-8353.84, A5=15269.4, A6=-84.7053,tipoffset=0, pushed=True)
	###################################################################

	
	machine.AddCircuit(type='phasor',name='pew', pushed=True)




	machine.Connect("scan.z" , "canti.holderz")
	machine.Connect("canti.zabs" , "Dimer.ztip")
	machine.Connect("Dimer.fz" , "canti.fz")
	


	machine.Connect('canti.ztip','amp.signal')
	machine.Connect('amp.amp','agc.signal')
	machine.Connect('amp.norm','pll.ref', 'pew.in1')
	#machine.Connect('wave.cos','pll.ref')
	machine.Connect('pll.cos','pll.vco','pew.in2')
	
	machine.Connect('agc.out','agclim.signal')
	machine.Connect('agclim.out','exc.in1')
	machine.Connect('pll.sin','pllinv.in1')
	machine.Connect('pllinv.out','exc.in2')
	
	machine.Connect('exc.out','canti.exciter')
	
    #Outputs
	out1 = machine.AddCircuit(type='output',name='output',file='testafm.out', dump=100)
	out1.Register('global.time', 'canti.zabs','pll.ref','pll.cos','pll.sin','exc.in2','pll.dbg')
	#out1.Register('global.time', 'wave.cos','pll.cos','pll.sin','exc.in2')
	

	out2 = machine.AddCircuit(type='output',name='output2',file='testafm2.out', dump=100)
	out2.Register('global.time', 'amp.amp','agc.out','pll.df','pew.delay',"canti.fz")

	out3 = machine.AddCircuit(type='output',name='output3',file='xe-kr-Dimer.out', dump=0)
	out3.Register("scan.z", "pll.df")
	out3.Stop()	


	machine.Connect("scan.record","output3.record")	

	out1.Stop()
	out2.Stop()

	scanner.Place(x=0,y=0,z=15)
	scanner.Move(x=0,y=0,z=-1)	
	machine.Wait(1)

	out3.Start()
	scanner.MoveRecord(x=0,y=0,z=-9.5,v=1,points=200)



'''
	machine.Wait(0.01)
	machine.circuits['wave'].I['freq'].Set(f0+14)
	machine.Wait(0.01)
	machine.circuits['wave'].I['freq'].Set(f0+20)
	machine.Wait(0.01)
'''


	#plot testafm.out 1:3 (canti) 1:4 (pll reference) 1:6 (the exciter)
	#u should see 3 distinct waves, canti peaks are in the middle between the other 2

if __name__ == '__main__':
        main()
