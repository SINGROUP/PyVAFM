#!/usr/bin/env python

from vafmcircuits import Machine


def main():

    machine = Machine(name='machine', dt=0.01, pushed=True)

    # Add Circuits
    machine.AddCircuit(type='waver', name='osc', amp=1, freq=1, pushed=True)
    machine.AddCircuit(type='derivative', name='der', pushed=True)
    machine.AddCircuit(type='integral', name='int', pushed=True)

    machine.Connect("osc.sin", "der.signal", "int.signal")

    out1 = machine.AddCircuit(
        type='output', name='output', file='test_derint.out', dump=2)
    out1.Register('global.time', 'osc.sin', 'osc.cos', 'der.out', 'int.out')

    machine.Wait(10)


if __name__ == '__main__':
    main()
