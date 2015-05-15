#!/usr/bin/env python
from vafmcircuits import Machine
from customs_pll import *
import math

machine = Machine(machine=None, name='Machine', dt=1e-8)

f0=350000
#nm
Az=0.3
Q=4
#N/m
k=4

machine.AddCircuit(type="Machine",name='LockInAmp', intTime=1.0/f0 * 1000, CentFreq=f0, gain=1 , Ampgain=2 ,assembly=LockInAmp, pushed=True)
#canti = machine.AddCircuit(type='Cantilever',name='canti', startingz=Az, Q=Q, k=k, f0=f0, pushed=True)
machine.AddCircuit(type='minmax', name='amp' , CheckTime = 1e-5)

machine.AddCircuit(type='waver',name='WaveGen', freq=f0 ,amp=1, pushed=True)


machine.AddCircuit(type='opAdd', name='summer', in2=0)

machine.Connect('WaveGen.cos','LockInAmp.Signal')
#machine.Connect('LockInAmp.RefWave','canti.exciter')
#machine.Connect('canti.ztip','amp.signal')

machine.Connect('summer.out','LockInAmp.CentFreq')



out1 = machine.AddCircuit(type='output',name='output',file='LockInTest.dat', dump=0)
#out1.Register('global.time','canti.ztip','LockInAmp.RefWave','LockInAmp.Amp','LockInAmp.Phase','amp.amp','summer.out')
out1.Register('summer.out','LockInAmp.Amp')


freq =f0-1000

while freq < (f0+1000):
	machine.SetInput(channel="summer.in1", value=freq)
	machine.Wait(0.1)
	out1.Dump()
	freq += 100
