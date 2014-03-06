#!/usr/bin/env python
import subprocess
import sys
sys.path.append('/Users/johntracey/Desktop/pyvafm-master/src')

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_signal_processing
import vafmcircuits_Filters

def main():
	
	#main machine
	machine = Machine(name='machine', dt=0.0001, pushed=True);
	
	# wave generator
	machine.AddCircuit(type='waver',name='wave', amp=1, pushed=True )
	
	#low-pass filter
	machine.AddCircuit(type='SKLP',name='sklp', fcut=100, pushed=True )
	#amplitude detector for the filter
	machine.AddCircuit(type='minmax', name='asklp', CheckTime=0.2, pushed=True)
	
	#high-pass filter
	machine.AddCircuit(type='SKHP',name='skhp', fcut=100, pushed=True )
	#amplitude detector for the filter
	machine.AddCircuit(type='minmax', name='askhp', CheckTime=0.2, pushed=True)
	
	#band-pass filter
	machine.AddCircuit(type='SKBP',name='skbp', fc=100, band=60, pushed=True )
	#amplitude detector for the filter
	machine.AddCircuit(type='minmax', name='askbp', CheckTime=0.2, pushed=True)

	#passive low pass filter
	machine.AddCircuit(type='RCLP',name='rclp', fc=100, order=100, pushed=True )
	#amplitude detector for the filter
	machine.AddCircuit(type='minmax', name='arclp', CheckTime=0.2, pushed=True)


	#passive high pass filter
	machine.AddCircuit(type='RCHP',name='rchp', fc=100, order=100, pushed=True )
	#amplitude detector for the filter
	machine.AddCircuit(type='minmax', name='archp', CheckTime=0.2, pushed=True)


	#connect oscillator to the filters
	machine.Connect("wave.sin","sklp.signal","skhp.signal","skbp.signal","rclp.signal","rchp.signal")
	machine.Connect("sklp.out","asklp.signal") #filter -> amplitude detector
	machine.Connect("skhp.out","askhp.signal") #filter -> amplitude detector
	machine.Connect("skbp.out","askbp.signal") #filter -> amplitude detector
	machine.Connect("rclp.out","arclp.signal") #filter -> amplitude detector
	machine.Connect("rchp.out","archp.signal") #filter -> amplitude detector
	
	#output to file - dump=0 means only manual dump
	out1 = machine.AddCircuit(type='output',name='output',file='filters.dat', dump=0)
	out1.Register('wave.freq', 'asklp.amp', 'askhp.amp', 'askbp.amp',"arclp.amp","archp.amp")
	
	
	#set the frequency and relax the filter
	freq = 5
	machine.SetInput(channel="wave.freq", value=freq)
	machine.Wait(1)
	
	
	while freq < 700:
	
		#assign the frequency to the oscillator
		machine.SetInput(channel="wave.freq", value=freq)
		
		#wait some time to charge the capacitors in the filters
		machine.Wait(0.5)
		
		out1.Dump() #output to file
		freq *= 1.2 #ramp the frequency
		
	

if __name__ == '__main__':
	main()

