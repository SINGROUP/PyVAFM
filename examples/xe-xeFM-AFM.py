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
	#xe-xe
	#dimer
	machine.AddCircuit(type='VDWtorn', name='Dimer',A1=0.624987, A2=0.42742, A3=1686.2, A4=-12092.2, A5=115496., A6=-115.753, tipoffset=0, pushed=True)

	#Surface
	machine.AddCircuit(type='VDWtorn', name='Pyramid',A1=-1987.09, A2=658.103, A3=-587.187, A4=21188.8, A5=-107670., A6=-26.6053,tipoffset=0, pushed=True)
 
	#Pyramid
	machine.AddCircuit(type='VDWtorn', name='Surface', A1=-883.96, A2=412.92, A3=1705.83, A4=-9119.11, A5=16490.2, A6=-87.6929,tipoffset=0, pushed=True)
	###################################################################

	
	machine.AddCircuit(type='phasor',name='pew', pushed=True)




	machine.Connect("scan.z" , "canti.holderz")
	machine.Connect("canti.zabs" , "Surface.ztip")
	machine.Connect("Surface.fz" , "canti.fz")
	


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

	out3 = machine.AddCircuit(type='output',name='output3',file='xe-xe-Surface.out', dump=0)
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
