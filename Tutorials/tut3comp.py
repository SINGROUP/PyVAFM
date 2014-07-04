from vafmbase import ChannelType
from vafmcircuits import Machine
import vafmcircuits


def ADC(compo,**keys):
	 
  	compo.AddInput("signal1")
  	compo.AddInput("signal2")
  	compo.AddOutput("out")
  	compo.AddCircuit(type='opAdd',name='adder')
  	compo.Connect("global.signal1","adder.in1")
  	compo.Connect("global.signal2","adder.in2")
  	compo.Connect("adder.out","global.out")
	
  	print "ADC assembled!"
