from vafmbase import ChannelType
from vafmcircuits import Machine
from tut3comp import *
import vafmcircuits



machine = Machine(name='machine', dt=0.01);

machine.AddCircuit(type='waver',name='osc', amp=1, freq=1)
  	
machine.AddCircuit(type='Machine', name='compo1', assembly=ADC)
  	
out1 = machine.AddCircuit(type='output',name='output',file='tut3.dat', dump=1)
out1.Register('global.time', 'osc.sin', 'compo1.out')
	
machine.Connect("osc.sin","compo1.signal1")
machine.Connect("osc.sin","compo1.signal2")
	
machine.Wait(5)