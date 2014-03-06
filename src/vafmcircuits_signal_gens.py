from collections import OrderedDict
from vafmbase import Circuit
from vafmbase import ChannelType
from vafmbase import Channel
import math


## \package vafmcircuits_signal_gens
# This module contains signal generator circuits (automatically imported).


## \brief Oscillator circuit.
#
# \image html waver.png "schema"
# Creates sine and cosine waves with the specifics given by the inputs.
# Can also create a sawtooth wave and a linear increasing signal (Ramper)
#
# \b Initialisation \b parameters:
# - pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# - \a amp = amplitude
# - \a freq = frequency
# - \a offset = offset value
#
# \b Output \b channels:
# - \a sin = \f$amp\cdot \sin(2 \pi freq\cdot t) + offset \f$  sine wave
# - \a cos = \f$amp\cdot \cos(2 \pi freq\cdot t) + offset \f$  cosine wave
# - \a saw = \f$amp\cdot( freq*f(t) - floor(freq*f(t) ) + offset \f$  sawtooth wave
#
# 
# \b Example:
# \code{.py}
# machine.AddCircuit(type='waver', name='wgen')
# machine.AddCircuit(type='waver', name='wgen', amp=1.2, freq=12000)
# \endcode
#
class waver(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("freq")
		self.AddInput("amp")
		self.AddInput("phi")
		self.AddInput("offset")
		

		self.AddOutput("sin")
		self.AddOutput("cos")
		self.AddOutput("saw")

		self.cCoreID = self.machine.cCore.Add_waver(self.machine.cCoreID)

		self.SetInputs(**keys)


		self.phase = 0

	def Initialize (self):

		pass




	def Update (self):
		pass
		'''
		self.phase += self.machine.dt * self.I["freq"].value
		
		phase = 2*math.pi*self.phase

		self.O['cos'].value = self.I['amp'].value*math.cos(phase) + self.I['offset'].value
		self.O['sin'].value = self.I['amp'].value*math.sin(phase) + self.I['offset'].value
		self.O['saw'].value = self.I['amp'].value * (self.machine.time *self.I["freq"].value - math.floor(self.machine.time *self.I["freq"].value)) + self.I['offset'].value
		
		if(self.phase >= 1): self.phase -= 1.0
		'''


## Digital square wave generator circuit.
#
# \image html square.png "schema"
# Creates sine and cosine waves with the specifics given by the inputs.
# Can also create a sawtooth wave and a linear increasing signal (Ramper)
#
# \b Initialisation \b parameters:
# - \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# - \a amp amplitude
# - \a freq = frequency
# - \a duty = length of duty cycle (1 full, 0 none)
# - \a offset = offset value
#
# \b Output \b channels:
# - \a out = square wave
#
# 
# \b Example:
# \code{.py}
# machine.AddCircuit(type='square', name='sqw')
# machine.AddCircuit(type='square', name='sqw', amp=1, freq=10)
# \endcode
#
class square(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("freq")
		self.AddInput("amp")
		self.AddInput("offset")
		self.AddInput("duty")

		self.AddOutput("out")

		self.cCoreID = self.machine.cCore.Add_square(self.machine.cCoreID)

		self.SetInputs(**keys)
		
		self.phase = 0

	def Initialize (self):
		
		pass




	def Update (self):

		self.phase += self.machine.dt * self.I["freq"].value
		#print self.phase, self.I['duty'].value
		
		if self.phase > self.I['duty'].value:
			self.O['out'].value = 0
		else:
			self.O['out'].value = 1

		if self.phase >= 1:
			self.phase -= 1
		
