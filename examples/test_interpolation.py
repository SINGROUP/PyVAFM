#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine
import vafmcircuits
import subprocess

import vafmcircuits_Filters
import vafmcircuits_Scanner
import vafmcircuits_Cantilever
import vafmcircuits_Interpolation


def main():

    machine = Machine(machine=None, name='machine', dt=0.001, pushed=False)

    scan = machine.AddCircuit(
        type='scanner', name='scann', Process=machine, pushed=False)
    inter = machine.AddCircuit(type='Interpolate', name='inter',
                               Filename='test_interpolation.dat', Dimensions=3, Components=3, pushed=False)
    inter.Minboundary(1, 1, 30)
    inter.Maxboundary(8, 8, 200)

    machine.Connect("scann.pos", "inter.coord")

    # Outputs
    out1 = machine.AddCircuit(
        type='output', name='output', file='test_interpolation.log', dump=1)
    out1.Register('global.time', 'inter.F1', 'inter.F2', 'inter.F3')

    scan.Place(1, 1, 30)
    scan.MoveTo(1, 1, 40, 0.1)


if __name__ == '__main__':
    main()
