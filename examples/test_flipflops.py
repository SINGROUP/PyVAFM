#!/usr/bin/env python

from vafmcircuits import Machine


def main():

    # main machine
    machine = Machine(name='machine', dt=0.01, pushed=True)

    # wave generator
    machine.AddCircuit(type='square', name='a', amp=1,
                       freq=2, offset=0.0, duty=0.1, pushed=True)
    machine.AddCircuit(type='square', name='b', amp=1,
                       freq=1.1, offset=0.0, duty=0.5, pushed=True)
    machine.AddCircuit(type='square', name='clock', amp=0.7,
                       freq=10, offset=0.0, duty=0.5, pushed=True)

    machine.AddCircuit(type='SRFlipFlop', name='SR', pushed=True)
    machine.AddCircuit(type='JKFlipFlop', name='JK', pushed=True)
    machine.AddCircuit(type='DFlipFlop', name='D', pushed=True)
    machine.AddCircuit(type='DRFlipFlop', name='DR', pushed=True)

    machine.Connect('clock.out', 'SR.clock', 'JK.clock', 'D.clock', 'DR.clock')
    machine.Connect('a.out', 'JK.J', 'SR.S', 'D.D', 'DR.D')
    machine.Connect('b.out', 'JK.K', 'SR.R', 'DR.R')

    # output to file - dump=0 means only manual dump
    out1 = machine.AddCircuit(
        type='output', name='output', file='test_flipflops.out', dump=1)
    out1.Register('global.time', 'a.out', 'b.out',
                  'clock.out', 'SR.Q', 'JK.Q', 'D.Q', 'DR.Q')

    machine.Wait(2)


if __name__ == '__main__':
    main()
