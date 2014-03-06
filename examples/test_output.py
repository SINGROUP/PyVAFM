#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	wave = machine.AddCircuit(type='waver',name='wave', amp=1, freq=2, pushed=True )
	outer= machine.AddCircuit(type='output', name='outer', file='test_output.log', dump=0 )
	outer.Register('global.time', 'wave.sin')

	machine.Connect('wave.sin','outer.record')
	
	machine.Wait(1)


if __name__ == '__main__':
	main()

