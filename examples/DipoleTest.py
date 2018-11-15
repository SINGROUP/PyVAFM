#!/usr/bin/env python
from vafmcircuits import Machine
from customs_pll import *


machine = Machine(machine=None, name='machine', dt=5.0e-8)


canti = machine.AddCircuit(type='Cantilever', name='canti',
                           startingz=2, Q=10000, k=167.0, f0=150000, pushed=True)


machine.AddCircuit(type="Machine", name='amp', fcut=10000,
                   assembly=aAMPD, pushed=True)

machine.AddCircuit(type='PI', name='agc', Kp=1.1, Ki=800, set=2, pushed=True)
machine.AddCircuit(type="limiter", name='agclim', min=-
                   100000, max=1000000, pushed=True)

machine.AddCircuit(type="Machine", name='pll', fcut=1000, assembly=aPLL, filters=[
                   10000, 5000, 2000], gain=600.0, f0=150000, Kp=0.5, Ki=700, pushed=True)

machine.AddCircuit(type='opMul', name='pllinv', in2=-1, pushed=True)
machine.AddCircuit(type='opMul', name='exc', pushed=True)

scanner = machine.AddCircuit(
    type='Scanner', name='scan', Process=machine, pushed=True)

inter = machine.AddCircuit(type='i3Dlin', name='inter', components=1)
inter.Configure(steps=[0.072049037037, 0.0748755555556,
                       0.075635735119], npoints=[216, 180, 335])
inter.Configure(pbc=[True, True, False])
inter.ReadData('testCeo2.dat')


# Outputs
out1 = machine.AddCircuit(type='output', name='output',
                          file='testafm.out', dump=2)
out1.Register('global.time', 'canti.zabs', 'amp.norm',
              'pll.cos', 'pll.sin', 'exc.in2')
out1.Stop()

out2 = machine.AddCircuit(type='output', name='output2',
                          file='testafm2.out', dump=1000)
out2.Register('global.time', 'canti.ztip', 'agc.out', 'pll.df', "canti.fz")
out2.Stop()

# Imaging output
imager = machine.AddCircuit(
    type='output', name='image', file='FMDipole.dat', dump=0)
imager.Register("scan.x", "scan.y", "pll.df")


# feed x and y to interpolation
machine.Connect("scan.x", "inter.x")
machine.Connect("scan.y", "inter.y")
machine.Connect("scan.z", "canti.holderz")
machine.Connect("canti.zabs", "inter.z")


# Force
machine.Connect("inter.F1", "canti.fz")

machine.Connect('canti.ztip', 'amp.signal')
machine.Connect('amp.amp', 'agc.signal')
machine.Connect('amp.norm', 'pll.signal1')
machine.Connect('pll.cos', 'pll.signal2')

machine.Connect('agc.out', 'agclim.signal')
machine.Connect('agclim.out', 'exc.in1')
machine.Connect('pll.cos', 'pllinv.in1')
machine.Connect('pllinv.out', 'exc.in2')

machine.Connect('exc.out', 'canti.exciter')

machine.Connect("scan.record", "image.record")


scanner.Place(x=0, y=0, z=18)
machine.Wait(0.1)


scanner.Move(x=0, y=0, z=-2)
machine.Wait(0.1)

scanner.Recorder = imager
scanner.BlankLines = True
# resolution of the image [# points per line, # lines]
scanner.Resolution = [128, 1]
scanner.ImageArea(16, 16)
# scan
scanner.ScanArea()
