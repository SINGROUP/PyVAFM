# -*- coding:utf-8 -*-

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_signal_processing
import vafmcircuits_Filters

def main():
	
	#main machine
	machine = Machine(name='machine', dt=0.00005, pushed=True);
	
	# wave generator
	machine.AddCircuit(type='waver',name='wave', amp=1, pushed=True )
	
	
	machine.AddCircuit(type='RCLP',name='sklp', fcut=100, order=1, pushed=True )
	#amplitude detector for the filter
	machine.AddCircuit(type='minmax', name='asklp', CheckTime=0.2, pushed=True)
	
	
	machine.AddCircuit(type='RCHP',name='skhp', fcut=100, order=1, pushed=True )
	#amplitude detector for the filter
	machine.AddCircuit(type='minmax', name='askhp', CheckTime=0.2, pushed=True)
	
	
	machine.AddCircuit(type='SKBP',name='skbp', fc=100, band=60, pushed=True )
	#amplitude detector for the filter
	machine.AddCircuit(type='minmax', name='askbp', CheckTime=0.2, pushed=True)

	#connect oscillator to the filters
	machine.Connect("wave.sin","sklp.signal","skhp.signal","skbp.signal")
	machine.Connect("sklp.out","asklp.signal") #filter -> amplitude detector
	machine.Connect("skhp.out","askhp.signal") #filter -> amplitude detector
	machine.Connect("skbp.out","askbp.signal") #filter -> amplitude detector
	
	#output to file - dump=0 means only manual dump
	out1 = machine.AddCircuit(type='output',name='output',file='test_filters2.log', dump=0)
	out1.Register('wave.freq', 'asklp.amp', 'askhp.amp', 'askbp.amp')
	
	
	#set the frequency and relax the filter
	freq = 5
	machine.SetInput(channel="wave.freq", value=freq)
	machine.Wait(1)
	
	while freq < 6000:
	
		#assign the frequency to the oscillator
		machine.SetInput(channel="wave.freq", value=freq)
		
		#wait some time to charge the capacitors in the filters
		machine.Wait(0.5)
		
		out1.Dump() #output to file
		freq *= 1.5 #ramp the frequency
		
	

if __name__ == '__main__':
	main()

