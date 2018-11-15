#!/usr/bin/env python

from vafmcircuits import Machine


def main():

    machine = Machine(name='machine', dt=0.01, pushed=True)

    # Add the circuits
    machine.AddCircuit(type='waver', name='osc', amp=1, freq=1.3, pushed=True)
    machine.AddCircuit(type='limiter', name='lim',
                       max=0.7, min=-0.3, pushed=True)

    machine.Connect("osc.sin", "lim.signal")

    out1 = machine.AddCircuit(
        type='output', name='output', file='test_limiter.out', dump=1)
    out1.Register('global.time', "osc.sin", "lim.out")

    machine.Wait(5)


if __name__ == '__main__':
    main()
