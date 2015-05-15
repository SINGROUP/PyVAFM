#!/usr/bin/env python
from vafmcircuits import Machine
from customs import *


def main():

	machine = Machine(machine=None, name='machine', dt=5.0e-8)
	canti = machine.AddCircuit(type='Cantilever',name='canti', 
		Q=20000, k=26.4, f0=150000, startingz=1, pushed=True)

	#machine.AddCircuit(type='waver',name='wave',freq=150000,amp=1)

	machine.AddCircuit(type="Machine",name='amp', fcut=10000, assembly=aAMPD, 
		pushed=True)
	
	machine.AddCircuit(type="PI",name='agc', Ki=2.1, Kp=0.1, set=10, pushed=True)
	machine.AddCircuit(type="limiter",name='agclim', min=0,max=10, pushed=True)
	
	machine.AddCircuit(type="Machine",name='pll', fcut=1000, assembly=dPFD, 
		gain=1000.0, f0=150000, KP=1.0, KI=100, pushed=True)
	
	machine.AddCircuit(type='opMul',name='pllinv',in2=-1, pushed=True)
	machine.AddCircuit(type='opMul',name='exc', pushed=True)
	
	machine.AddCircuit(type='phasor',name='pew', pushed=True)
	
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
	out1 = machine.AddCircuit(type='output',name='output',file='testafm.out', dump=2)
	out1.Register('global.time', 'canti.zabs','amp.norm','pll.cos','pll.sin','exc.in2','pll.dbg')
	#out1.Register('global.time', 'wave.cos','pll.cos','pll.sin','exc.in2')
	out1.Stop()

	out2 = machine.AddCircuit(type='output',name='output2',file='testafm2.out', dump=100)
	out2.Register('global.time', 'amp.amp','agc.out','pll.df','pew.delay')

	machine.Wait(0.01)
	out1.Start()
	machine.Wait(0.001)
	out1.Stop()

	machine.Wait(0.05)
	out1.Start()
	machine.Wait(0.001)

	#plot testafm.out 1:3 (canti) 1:4 (pll reference) 1:6 (the exciter)
	#u should see 3 distinct waves, canti peaks are in the middle between the other 2

if __name__ == '__main__':
        main()

