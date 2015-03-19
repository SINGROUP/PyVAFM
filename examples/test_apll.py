#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
#import vafmcircuits_control
#import vafmcircuits_Filters
from customs_pll import *


def main():
	
	f0=1.0e4
	
	machine = Machine(name='machine', dt=5.0e-8, pushed=True);
	
	machine.AddCircuit(type='waver',name='osc', amp=1, freq=f0+4, pushed=True)
	machine.AddCircuit(type="Machine",name='pll', assembly=aPLL, filters=[10000,5000,2000],
		gain=600.0, f0=f0, Kp=0.5, Ki=800, pushed=True)
	
  	
	machine.Connect("osc.cos","pll.signal1")
	machine.Connect("pll.sin","pll.signal2")
	
	
	out1 = machine.AddCircuit(type='output',name='output',file='test_apll.log', dump=200)
	out1.Register('global.time', 'pll.signal1', 'pll.signal2', 'pll.df')
	
	machine.Wait(0.01)
	machine.circuits['osc'].I['freq'].Set(f0+14)
	machine.Wait(0.01)
	machine.circuits['osc'].I['freq'].Set(f0-100)
	machine.Wait(0.01)
	machine.circuits['osc'].I['freq'].Set(f0-300)
	machine.Wait(0.01)
		
if __name__ == '__main__':
	main()

