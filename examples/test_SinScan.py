#!/usr/bin/env python

from vafmcircuits import Machine


machine = Machine(name='machine', dt=0.001, pushed=True)


# Add Circuits
scanner = machine.AddCircuit(type='Scanner', name='scan', pushed=True)


out1 = machine.AddCircuit(type='output', name='output',
                          file='sintest.dat', dump=1)
out1.Register("global.time", "scan.z")


scanner.Place(x=1, y=3.5, z=42.5)
scanner.SinScan(amp=2, freq=1, cycles=3)
