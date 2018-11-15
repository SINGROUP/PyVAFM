#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_Logic


def compomaker(compo, **keys):

    compo.AddInput("signal1")
    compo.AddInput("signal2")
    compo.AddOutput("out")
    compo.AddCircuit(type='opAdd', name='adder', factors=2, pushed=True)
    compo.Connect("global.signal1", "adder.in1")
    compo.Connect("global.signal2", "adder.in2")
    compo.Connect("adder.out", "global.out")

    print("ADC assemb led!")


def main():

    machine = Machine(name='machine', dt=0.01, pushed=True)

    wave = machine.AddCircuit(
        type='waver', name='wave', amp=1, freq=1, pushed=True)
    adder = machine.AddCircuit(type='opAdd', name='add', pushed=True)
    compo = machine.AddCircuit(
        type='Machine', name='compo', assembly=compomaker, pushed=True)

    outer = machine.AddCircuit(
        type='output', name='outer', file='test_cCore.log', dump=1)

    outer.Register('global.time', 'wave.cos', 'wave.sin', 'add.out')

    # print wave.cCoreID
    # print machine.cCoreID
    # machine.cCore.DebugCircuit(machine.cCoreID)
    # print wave.cCoreID
    # print machine.cCoreO

    machine.cCore.DebugCircuit(wave.cCoreID)

    machine.cCore.DebugCircuit(adder.cCoreID)
    machine.Connect('wave.cos', 'add.in1')
    machine.Connect('wave.sin', 'add.in2')

    machine.cCore.DebugCircuit(adder.cCoreID)
    # machine.cCore.DebugCircuit(1)
    # machine.cCore.DebugCircuit(2)

    # for i in range(len(wave.I)):
    #    print i,wave.I.values()[i].signal.cCoreFEED

    machine.Wait(1.03)

    machine.cCore.DebugCircuit(wave.cCoreID)

    """
	#Add Circuits
	machine.AddCircuit(type='square',name='s1', amp=1, freq=1, duty=0.5, pushed=True )
	machine.AddCircuit(type='square',name='s2', amp=1, freq=2.5, duty=0.2, pushed=True )
  	
	machine.AddCircuit(type='NOT',name='not', pushed=True )
	machine.AddCircuit(type='AND',name='and', pushed=True )
	machine.AddCircuit(type='OR',name='or', pushed=True )
	machine.AddCircuit(type='XOR',name='xor', pushed=True )
	machine.AddCircuit(type='NOR',name='nor', pushed=True )
	
	machine.Connect("s1.out","not.signal")
	machine.Connect("s1.out","and.in1","or.in1","xor.in1","nor.in1")
	machine.Connect("s2.out","and.in2","or.in2","xor.in2","nor.in2")
	
	
	out1 = machine.AddCircuit(type='output',name='output',file='test_logic.log', dump=1)
	out1.Register('global.time', 's1.out', 's2.out','not.out','and.out','or.out','xor.out','nor.out')
	
	for i in range(1000):
	    machine.Update()
	"""


if __name__ == '__main__':
    main()
