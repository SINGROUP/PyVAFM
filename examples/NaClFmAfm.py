#!/usr/bin/env python

from vafmcircuits import Machine
from customs import *


def main():

    machine = Machine(name='machine', dt=5e-8, pushed=True)
    f0 = 100000.0

    # Add Circuits
    canti = machine.AddCircuit(type='Cantilever', name='canti', startingz=0.5,
                               Q=10000, k=167.0, f0=f0, pushed=True)

    machine.AddCircuit(type='delay', name='phi', DelayTime=0.5/f0, pushed=True)
    machine.AddCircuit(type='Machine', name='ampd',
                       assembly=aAMPD, fcut=10000, pushed=True)
    machine.AddCircuit(type='PI', name='agc', Kp=1.1,
                       Ki=800, set=1, pushed=True)

    machine.AddCircuit(type='Machine', name='pll', assembly=aPLL, filters=[10000, 5000, 2000],
                       gain=500.0, f0=f0, Kp=0.5, Ki=800, pushed=True)
    machine.AddCircuit(type='opMul', name='exciter', pushed=True)

    #machine.AddCircuit(type='waver', name='wave', freq=100000.0, pushed=True)
    scanner = machine.AddCircuit(
        type='Scanner', name='scan', Process=machine, pushed=True)

    inter = machine.AddCircuit(
        type='i3Dlin', name='inter', components=3, pushed=True)
    inter.Configure(
        steps=[0.805714285714286, 0.805714285714286, 0.1], npoints=[8, 8, 171])
    inter.Configure(pbc=[True, True, False])
    inter.Configure(ForceMultiplier=1e10)
    inter.ReadData('NaClforces.dat')

    # Imaging output
    imager = machine.AddCircuit(
        type='output', name='image', file='NaCl.dat', dump=0)
    imager.Register("scan.x", "scan.y", "pll.df")

    # Debug output
    #out1 = machine.AddCircuit(type='output',name='output',file='Debug.dat', dump=1)
    #out1.Register('global.time', "scan.x", "scan.y", "scan.z", 'image.record',"canti.zabs")

# feed x and y to interpolation
    machine.Connect("scan.x", "inter.x")
    machine.Connect("scan.y", "inter.y")

# feed z to cantilever then the ztip of canti to interpolation
    machine.Connect("scan.z", "canti.holderz")
    machine.Connect("canti.zabs", "inter.z")

# feed force to canti
    machine.Connect("inter.F3", "canti.fz")

    machine.Connect('canti.ztip', 'ampd.signal')
    machine.Connect('ampd.amp', 'agc.signal')

    machine.Connect("ampd.norm", "phi.signal")
    machine.Connect("phi.out", "pll.signal1")
    machine.Connect("pll.cos", "pll.signal2")

    machine.Connect('agc.out', 'exciter.in1')
    machine.Connect('pll.cos', 'exciter.in2')
    machine.Connect('exciter.out', 'canti.exciter')

    machine.Connect("scan.record", "image.record")

    #machine.SetInput(channel="output.record", value=0)

    scanner.Place(x=0.805714285714286, y=0.805714285714286, z=4.5)

    scanner.Move(x=0, y=0, z=-0.5)
    machine.Wait(0.02)

    #machine.SetInput(channel="output.record", value=1)
    scanner.Recorder = imager
    scanner.BlankLines = True
    # resolution of the image [# points per line, # lines]
    scanner.Resolution = [64, 1]
    scanner.ImageArea(11.68, 11.68)
    # scan
    scanner.ScanArea()


if __name__ == '__main__':
    main()
