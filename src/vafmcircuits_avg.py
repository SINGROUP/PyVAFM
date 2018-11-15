from vafmbase import Circuit
from vafmbase import ChannelType
from vafmbase import Channel
from ctypes import c_int

import math
import numpy

## \package vafmcircuits_avg
# This file contains the averager circuit classes.

## \brief Averager circuit.
#
# \image html Avg.png "schema"
# This circuit will return the average of an input signal, over a certain amount of time.
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
# 	- \a time = sampling time (in real time units)
#	- \a moving = True|False  compute average at each step (True) or only when the buffer is full (False, default)
#
# \b Input \b channels:
# 	- \a signal =  signal to average
#
# \b Output \b channels:
# 	- \a out = averaged signal
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='avg', name='average', time = 10, moving = False , pushed = 'True')
# \endcode
#
class avg(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("signal")
		self.AddOutput("out")

		self._time = 0.01
		self._steps = 10
		self._cnt = 0
		self._moving = False
		
		if 'time' in list(keys.keys()):
			self._time = float(keys['time'])
		else:
			raise NameError("Missing time parameter!")
		
		self._steps = math.floor(self._time/self.machine.dt)
		self._buffer = numpy.zeros(self._steps)
		
		if 'moving' in list(keys.keys()):
			self._moving = bool(keys['moving'])

		m = c_int(0);
		if(self._moving == True):
			m = c_int(1)
		
		self.cCoreID = Circuit.cCore.Add_avg(machine.cCoreID, int(self._steps), m)

		
		self.SetInputs(**keys)

		self.tot = 0

	def Initialize (self):

		pass
	

	def Update (self):
		pass


