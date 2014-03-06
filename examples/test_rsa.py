#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_rsa
from customs_pll import *

'''
center of mass position: (x,y,z) = (0, 0, 0.022m)
total mass: 0.0255kg
moment of inertia : 4.62e-6 kgm^2
positions of the springs attached :
 (x,y,z) = (-0.0141m, 0, 0.0249m) and (0.0141m, 0, 0.0249m) 
'''

def main():
	
	f0 = 30
	
	machine = Machine(name='machine', dt=1.0e-5, pushed=True);
	
	scan= machine.AddCircuit(type='Scanner', name='scan', pushed=True)
	exc = machine.AddCircuit(type='waver',name='exc', amp=1, freq=f0, pushed=True)
	
	rsa = machine.AddCircuit(type='RSA', name='rsa', eta=0.1, pushed=True)
	rsa.SetSprings(860,15000,7000)
	rsa.SetPoints(0.0141,0.0029,-0.022)
	rsa.SetGammas(0.066, 0.2, 0.1)
	rsa.SetMasses(0.0255, 0.06, 4.62e-6)
	
	
	
	machine.AddCircuit(type='Machine', name='amp', assembly=aAMPD, fcut=4, pushed=True)
 	
 	machine.Connect("scan.x","exc.freq")
 	machine.Connect("scan.y","exc.amp")
 	machine.Connect("scan.z","rsa.eta")
	machine.Connect("exc.cos","rsa.exciter")
	machine.Connect("rsa.xcm","amp.signal")
	
	
	#out1 = machine.AddCircuit(type='output',name='output',file='test_rsa.log', dump=4)
	#out1.Register('global.time','exc.cos')


	scan.Place(x=30,y=1,z=0.0)
	machine.Wait(2.0)
	
	out2 = machine.AddCircuit(type='output',name='res',file='test_rsa2.log', dump=1000)
	out2.Register('exc.freq', 'amp.amp')	
	
	for eta in [0.0, 0.1, 0.5, 1.0]:
		out2.Stop()
		scan.Place(x=30,y=1,z=eta)
		machine.Wait(2.0)
		out2.Start()
		scan.MoveTo(x=80, v=0.1)
	
	
	
	
if __name__ == '__main__':
	main()

