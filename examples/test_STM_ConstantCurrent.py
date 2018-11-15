#!/usr/bin/env python
from vafmcircuits import Machine


def main():
    I = 3e-8

    machine = Machine(machine=None, name='machine', dt=1e-3)

    scanner = machine.AddCircuit(type='Scanner', name='scan', pushed=True)

    machine.AddCircuit(type='PI', name='pi', Kp=-1.1,
                       Ki=-800, set=I, pushed=True)
    machine.AddCircuit(type='opAdd', name='Add', pushed=True)
    machine.AddCircuit(type='opMul', name='Scaler', in2=10000, pushed=True)

    machine.AddCircuit(type="limiter", name='lim', min=9, max=20, pushed=True)

    inter = machine.AddCircuit(
        type='i4DlinVasp', name='inter', components=1, pushed=True)
    inter.BiasStep = 0.5
    inter.StartingV = 2
    inter.ConfigureVASP(pbc=[True, True, False, False])
    inter.ReadVASPData("parchg.2.0")

    machine.AddCircuit(type='STM', name='STM', pushed=True)

    out1 = machine.AddCircuit(
        type='output', name='output', file='testSTM.dat', dump=100)
    out1.Register('global.time', 'scan.x', 'inter.z',
                  'Add.out', 'STM.Current', 'inter.F', 'pi.out')

    imager = machine.AddCircuit(
        type='output', name='image', file='STM.dat', dump=0)
    imager.Register("scan.x", "scan.y", 'STM.Current',
                    'inter.F', 'pi.out', "inter.z")

    machine.Connect("scan.x", "inter.x")
    machine.Connect("scan.y", "inter.y")
    # machine.Connect("scan.z","inter.z")

    machine.Connect("pi.out", "Scaler.in1")

    machine.Connect("Add.out", "lim.signal")
    machine.Connect("lim.out", "inter.z")

    machine.Connect("inter.F", "STM.Density")
    machine.Connect("scan.record", "image.record")
    machine.Connect("STM.Current", "pi.signal")

    machine.Connect("scan.z", "Add.in1")
    machine.Connect("Scaler.out", "Add.in2")

    machine.circuits['inter'].I['V'].Set(2)
    scanner.Place(x=0, y=4, z=15)
    machine.Wait(2)

#	scanner.Move(x=18,y=0,z=0)

    '''
	machine.circuits['pi'].I['signal'].Set(1)
	machine.Wait(0.1)
	machine.circuits['pi'].I['signal'].Set(2)
	machine.Wait(0.1)
	machine.circuits['pi'].I['signal'].Set(0.1)
	machine.Wait(0.1)
	'''

    scanner.Recorder = imager
    scanner.BlankLines = True
    FastSpeed = 0.4
    # resolution of the image [# points per line, # lines]
    scanner.Resolution = [200, 200]
    scanner.ImageArea(18, 9)
    # scan
    scanner.ScanArea()


if __name__ == '__main__':
    main()
