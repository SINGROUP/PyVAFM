#!/usr/bin/env python

from vafmcircuits import Machine
from customs_pll import *


def main():

    machine = Machine(name='machine', pushed=True, dt=0.001)

    # Add Circuits
    canti = machine.AddCircuit(
        type='Cantilever', name='canti', startingz=5, Q=300, k=1, f0=50, pushed=True)

    out1 = machine.AddCircuit(
        type='output', name='output', file='cantilever.dat', dump=1)
    out1.Register("global.time", "canti.ztip")

    machine.Wait(2)


if __name__ == '__main__':
    main()
