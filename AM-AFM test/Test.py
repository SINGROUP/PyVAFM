#!/usr/bin/env python
from vafmcircuits import Machine
from customs_pll import *

#A = 9.75
#A = 9.82
A=0.98
machine = Machine(machine=None, name='machine', dt=5.0e-8)


scanner = machine.AddCircuit(type='Scanner',name='scan', Process = machine, pushed=True)


canti = machine.AddCircuit(type='Cantilever',name='canti', startingz=0.5,
	Q=4, k=4.0, f0=1500, pushed=True)


machine.AddCircuit(type='phasor', name='Phasor' )

#+ve force grad gives a -ve freq shift moving the canti further from res and hence reducing amp...
#10
machine.AddCircuit(type='waver',name='wave',freq=1000 ,amp=0.5,offset=0)


machine.AddCircuit(type="Machine",name='amp', fcut=100, assembly=aAMPD, pushed=True)



    #Outputs
out1 = machine.AddCircuit(type='output',name='output',file='test.out', dump=10000)
out1.Register('global.time','amp.amp','canti.ztip','Phasor.delay')


machine.Connect('wave.sin','canti.exciter')
machine.Connect('canti.ztip','amp.signal')

machine.Connect('canti.ztip','Phasor.in1')
machine.Connect('wave.sin','Phasor.in2')


machine.Wait(0.1)
