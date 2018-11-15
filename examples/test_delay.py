#!/usr/bin/env python

from vafmcircuits import Machine


def main():

    machine = Machine(name='machine', dt=0.01, pushed=True)

    # Add Circuits
    machine.AddCircuit(type='waver', name='osc', amp=1, freq=1, pushed=True)
    machine.AddCircuit(type='delay', name='lag', DelayTime=0.2, pushed=True)

    machine.Connect("osc.sin", "lag.signal")

    out1 = machine.AddCircuit(
        type='output', name='output', file='test_delay.out', dump=1)
    out1.Register('global.time', 'osc.sin', 'lag.out')

    machine.Wait(5)


if __name__ == '__main__':
    main()
