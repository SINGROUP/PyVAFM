##!/usr/bin/env python
import subprocess
import sys
sys.path.append('/Users/johntracey/Desktop/pyvafm-master/src')

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits


def main():
	
	#main machine
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	# wave generator
	machine.AddCircuit(type='waver',name='wave', amp=1, freq=2, phi=0, offset=0, pushed=True)
	machine.AddCircuit(type='square',name='sqw', amp=0.7, freq=10, offset=0.0, duty=0.5, pushed=True )

	machine.AddCircuit(type='SRFlipFlop', name='SR', pushed=True)
	machine.AddCircuit(type='JKFlipFlop', name='JK', pushed=True)
	machine.AddCircuit(type='DFlipFlop', name='D', pushed=True)
	machine.AddCircuit(type='DRFlipFlop', name='DR', pushed=True)



	#output to file - dump=0 means only manual dump
	out1 = machine.AddCircuit(type='output',name='output',file='flipflops.dat', dump=1)
	out1.Register('global.time', 'wave.sin', 'wave.cos', 'sqw.out', 'D.Q')
	


	machine.Connect('wave.sin','D.D')
	machine.Connect('wave.cos','JK.K')
	machine.Connect('sqw.out','D.clock')
	
	machine.Wait(1)
	
	

if __name__ == '__main__':
	main()

