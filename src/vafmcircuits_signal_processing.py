from vafmbase import Circuit
from ctypes import *
import math
import vafmcircuits

## \package vafmcircuits_signal_processing
# This file contains the signal processing circuits for example min/max and delay.
#


## \brief Gain circuit.
#
# \image html gain.png "schema"
# Takes in an input signal and multiplies it by a given gain
# 
#
# \b Initialisation \b parameters:
# - pushed = True|False  push the output buffer immediately if True
# - gain = integer 
#
# \b Input \b channels:
# - \a signal 
#
# \b Output \b channels:
# - \a out =  signal \f$ \cdot \f$ gain 
#
# 
# \b Example:
# \code{.py}
# machine.AddCircuit(type='gain', name='Gain' , gain = 10)
# \endcode
#
class gain(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("signal")
		self.AddOutput("out")

		if 'gain' in keys.keys():
			self.gain = keys['gain']
		else:
			raise NameError("Missing gain parameter!")

		self.cCoreID = Circuit.cCore.Add_gain(self.machine.cCoreID, c_double(self.gain))
		
		self.SetInputs(**keys)

	def Initialize (self):

		pass


	def Update (self):		
		self.O['out'].value  = self.I['signal'].value*self.gain



## \brief Min/Max circuit.
#
# \image html minmax.png "schema"
# Takes in an input signal and multiplies it by a given gain
# 
#
# \b Initialisation \b parameters:
# - pushed = True|False  push the output buffer immediately if True
# - CheckTime = length of time interval where a max and min value will detected. 
# 				After this period has elapsed the circuit will output and 
#				then will begin checking for mins and maxs during the next interval.
#
# \b Input \b channels:
# - \a signal 
#
# \b Output \b channels:
# - \a max =  Maximum value found in the CheckTime interval
# - \a min =  Minimum value found in the CheckTime interval
# - \a amp =\f$ \frac{max - min}{2}\f$
# - \a offset = \f$ \frac{max + min}{2}\f$
#
# 
# \b Example:
# \code{.py}
# machine.AddCircuit(type='minmax', name='MinandMax' , CheckTime = 4)
# \endcode
#
class minmax(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )
		#check if checktime is used in the input file
		if 'CheckTime' in keys.keys():
			self.checktime = keys['CheckTime']
		else:
			raise NameError("Missing CheckTime input!")
		#calculate how many steps are needed for the given timestep
		self.timesteps = int(self.checktime/self.machine.dt)

		self.counter=0

		self.AddInput("signal")

		#create output channels
		self.AddOutput("max")
		self.AddOutput("min")
		self.AddOutput("amp")
		self.AddOutput("offset")

		self.cCoreID = Circuit.cCore.Add_minmax(self.machine.cCoreID, c_double(self.checktime))

		self.SetInputs(**keys)

		#setting min and max to the first value in the input file
		#self.min=self.I["signal"].value
		#self.max=self.I["signal"].value

	def Initialize (self):

		pass

	def Update (self):
		pass
		"""
		#if the value is greater or less than min or max then reassign the max and min values
		if self.I["signal"].value > self.max:
			self.max=self.I["signal"].value
		if self.I["signal"].value < self.min:
			self.min=self.I["signal"].value
		#add one to the counter
		self.counter=self.counter + 1
		#only print out values that are not 0 when the counter is = to timesteps
		#self.O['max'].value = 0
		#self.O['min'].value = 0

		#if the counter is equal to the amount of time steps then then output the values
		if self.timesteps == self.counter:

			self.O['max'].value = self.max
			self.O['min'].value = self.min

			self.O['amp'].value = (self.max - self.min)/2
			self.O['offset'].value = (self.max + self.min)/2

			#reset min and max for the next calculation
			self.min=self.I["signal"].value
			self.max=self.I["signal"].value


			self.counter=0
		"""


## \brief Differentation circuit.
#
# \image html derivative.png "schema"
# Takes in a input and returns the derivative
#
# \b Initialisation \b parameters:
#	- \a pushed = True|False  push the output buffer immediately if True
#	
#
# \b Input \b channels: 
# 	- \a signal
#
# \b Output \b channels: 
# 	- \a out =  \f$ \frac{din}{dt} \f$ = \f$ \frac{f(t)-f(t-1)}{dt} \f$ 
#
# \b Example:
# \code
# machine.AddCircuit(type='derivative', name='Differentation')
# \endcode
#
class derivative(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("signal")

		#create output channels
		self.AddOutput("out")

		self.cCoreID = self.machine.cCore.Add_derivative(self.machine.cCoreID)

		self.SetInputs(**keys)


		#@todo i dont understand this it should always be 0 anyway!
		self.y=self.I["signal"].value
		self.yo = 0

	def Initialize (self):

		pass



	def Update (self):
		pass
		"""
		self.yo=self.y
		self.y = self.I["signal"].value

		result=(self.y-self.yo)/(self.machine.dt)

		self.O['out'].value = result
		"""

## \brief Integration circuit.
#
# \image html integral.png "schema"
# Takes in a input and returns the integral using the Trapezoidal rule
#
# \b Initialisation \b parameters: 
# 	- \a pushed = True|False  push the output buffer immediately if True
#	
#
# \b Input \b channels: 
# 	- \a signal
#
# \b Output \b channels: 
# 	- \a out = \f$ \int_0^t in\f$ \f$dt \f$
#
# \b Example:
# \code
# machine.AddCircuit(type='integral', name='Integration')
# \endcode
class integral(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("signal")

		#create output channels
		self.AddOutput("out")

		self.cCoreID = self.machine.cCore.Add_integral(self.machine.cCoreID)

		self.SetInputs(**keys)

		self.yo=0
		self.result = 0

	def Initialize (self):

		pass




	def Update (self):
		pass
		"""
		self.result +=  ( (self.yo + self.I["signal"].value)*(self.machine.dt)*0.5 )

		self.O['out'].value = self.result
		self.yo = self.I["signal"].value
		"""

## \brief Delay circuit.
#
# \image html Delay.png "schema"
# Takes in a input and delays the start of the circuit by a fixed amount of inputted time
#
# \b Initialisation \b parameters:
# 	- \a pushed    = True|False  push the output buffer immediately if True
#	- \a DelayTime = Integer
#
# \b Input \b channels:
# 	- \a signal
#
#
# \b Output \b channels:
# 	- \a out = \f$In_{t-DelayTime}\f$
#
# \b Example:
# \code
# machine.AddCircuit(type='delay', name='delay' , DelayTime=2)
# \endcode
#
class delay(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("signal")
		self.AddOutput("out")

		if 'DelayTime' in keys.keys():
			self.delaytime = keys['DelayTime']
		else:
			raise NameError("Missing DelayTime input!")

		self.steps = int(self.delaytime/self.machine.dt)
		#self.counter = 0
		#self.counteroutput = 0

		#self.bufferinput = []
		
		self.cCoreID = Circuit.cCore.Add_delay(machine.cCoreID, self.steps)
		
		self.SetInputs(**keys)
		



	def Initialize (self):
		pass




	def Update (self):
		pass
		"""
		if self.counter * self.machine.dt <= self.delaytime:
			self.O["out"].value = 0

		self.bufferinput.append(self.I["signal"].value)
		self.counter = self.counter + 1

		if self.counter * self.machine.dt  > self.delaytime: 
			self.O["out"].value = self.bufferinput[self.counteroutput]

			self.counteroutput = self.counteroutput+1
		"""


##\brief Peak Detector circuit.
#
# \image html PeakDetector.png "schema"
# Takes in an input and outputs when it finds a peak, where the peak is and how long since the last peak
# - Upper Peak found if \f$(t-2)\f$ \f$<\f$ \f$f(t-1)\f$ and \f$f(t-1)\f$ \f$>\f$ \f$f(t)\f$  is true
# - Lower Peak found if \f$(t-2)\f$ \f$>\f$ \f$f(t-1)\f$ and \f$f(t-1)\f$ \f$<\f$ \f$f(t)\f$ is true
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#	- \a up     = 1|0 : When set to 1 peaks in the positve y axis will be detected and when set to 0 peaks in the negative will be detected.
#
# \b Input \b channels:
# 	- \a signal
#
# \b Output \b channels:
# 	- \a tick  = 1 if a peak and 0 if no peak 
# 	- \a peak  = location of the peak
# 	- \a delay = time elapsed since last peak was found
#
# \b Example:
# \code
# machine.AddCircuit(type='peaker', name='Peaks' , up = 1)
# \endcode
#
class peaker(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )

		if 'up' in keys.keys():
			self.up = keys['up']
			if self.up == 1:
				self.upordown=True
			if self.up == 0:
				self.upordown = False

		else:
			raise NameError("Missing up or down selection!")
		
		self.AddInput("signal")
		self.AddOutput("peak")
		self.AddOutput("tick")
		self.AddOutput("delay")

		self.cCoreID = Circuit.cCore.Add_peaker(machine.cCoreID, self.up)
		
		self.SetInputs(**keys)

		"""
		self.counter=0
		self.yoo=0
		self.yo=0
		self.y=0

		self.peak = 0
		self.tick = 0
		self.delay = 0
		self.startcounter = False
		"""

	def Initialize (self):
		pass


	def Update (self):
		pass
		"""
		self.yoo= self.yo
		self.yo = self.y
		self.y= self.I["signal"].value
		self.tick=0

		if self.yoo < self.yo and self.yo > self.y and self.upordown == True:
			self.tick = 1 
			self.peak = self.yo
			self.delay = self.counter * self.machine.dt
			self.counter=0

		if self.yoo > self.yo and self.yo < self.y and self.upordown == False:
			self.tick = 1  
			self.peak= self.yo
			self.delay = self.counter * self.machine.dt
			self.counter = 0

		self.counter=self.counter + 1

		self.O["peak"].value = self.peak
		self.O["tick"].value = self.tick
		self.O["delay"].value = self.delay
		"""
		

##\brief Phasor circuit.
## \image html Phasor.png "schema"
# Takes in two inputs and will measure the legnth of time between the first
# input becoming postive and the second also becoming positive.
#
#- \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- \a in1
#	- \a in2
#
# \b Output \b channels:
# 	- \a tick = 1 when input 2 becomes positve assuming input 1 has alreayd become postive before it
# 	- \a delay = time difference between input 1 and input 2 becoming positve 
#
# \b Example:
# \code
# machine.AddCircuit(type='phasor', name='Phasor' )
# \endcode
#
class phasor(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )
		self.AddInput("in1")
		self.AddInput("in2")
		self.AddOutput("tick")
		self.AddOutput("delay")
		
		self.counter= 0
		self.check = False
		
		self.cCoreID = Circuit.cCore.Add_phasor(machine.cCoreID)
		
		self.SetInputs(**keys)

	def Initialize (self):

		pass




	def Update (self):
		pass
		"""
		if	self.I["in1"].value > 0 and self.I["in2"].value < 0:
			self.counter = self.counter +1
			self.check= True

		#@todo are you sure these 2 lines should not be indented under the if?
		self.O["tick"].value = 0
		self.O["delay"].value = 0

		if self.I["in2"].value > 0 and self.check == True:
			self.O["tick"].value = 1
			self.O["delay"].value = self.counter * self.machine.dt
			self.counter = 0
			self.check = False
		"""

##  \brief Limiter circuit.
#
# \image html Limiter.png "schema"
# This circuit will limit a signal from going above the max and below the min values.
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels: 
# 	- \a signal = incoming signal
# 	- \a min = minimum value
# 	- \a max = maximum value
#
# \b Output \b channels:
# 	- \a out = \f$ \mbox{Max}(\mbox{Min}(signal, max), min)\f$
#
# \b Example:
# \code{.py}
# machine.AddCircuit(type='limiter', name='lim')
# machine.AddCircuit(type='limiter', name='lim', min=-10.0)
# machine.AddCircuit(type='limiter', name='lim', min=0.0, max=99999)
# \endcode
#
class limiter(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("signal")
		self.AddInput("max")
		self.AddInput("min")
		self.AddOutput("out")

		self.cCoreID = Circuit.cCore.Add_limiter(machine.cCoreID)

		self.SetInputs(**keys)

	def Initialize (self):

		pass


	def Update (self):
		pass
		"""
		self.O["out"].value =  max(min(self.I["signal"].value, self.I["max"].value), 
			self.I["min"].value)
		"""


## \brief Flip circuit.
#
## \image html Flip.png "schema"
# Takes in an input and will output a tick everytime the signal changes 
# from negative to positive.
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- \a signal
#
# \b Output \b channels:
# 	- \a out = 1 when \f$f(t-1)\f$ \f$<=\f$ 0 and \f$f(t)\f$ \f$>\f$ 0
#
# \b Example:
# \code
# machine.AddCircuit(type='flip', name='Flip')
# \endcode
#
class flip(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )
		self.AddInput("signal")
		self.AddOutput("tick")
		self.yo= 0
		
		self.cCoreID = Circuit.cCore.Add_flip(machine.cCoreID)
		
		self.SetInputs(**keys)
	
		
	def Initialize (self):
		pass
	
	def Update (self):
		pass



