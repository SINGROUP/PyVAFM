from vafmbase import Circuit
import math, time
#from vafmcircuits import Machine
from ctypes import c_double

## \package vafmcircuits_Filters
# This file contains the Filters


## \brief Active Low Pass Filter circuit.
#
#
# \image html ActiveLowPass.png "schema"
# Takes a signal in and passes it through a low pass filter using the Sallen-Key topology
#
# \b Initialisation \b parameters:
# 	- \a gain =  Integer:  How much gain the signal will recive 
# 	- \a Q = the Q value of the filter
#	- \a fc = the frequency cut off for the circuit
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- signal =  incoming signal
#
# \b Output \b channels:
# 	- \a out = \f$  G \cdot \frac{x(s)}{s^{2} + \frac{ \omega_{c} }{Q} \cdot s + \omega^{2}_{c} } \f$ where \f$ x \f$ is the input signal,  \f$ \omega_{c} = 2 \pi f_c \f$ is the cut off pulse
# 	  \f$ Q \f$  is the quality factor and \f$ G \f$ is the gain.
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='SKLP', name='filter', fc=150)
# machine.AddCircuit(type='SKLP', name='filter', gain=10, Q=2, fc=50, pushed='True')
# \endcode
#
class SKLP(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("signal")
		self.AddOutput("out")


		self.Gain=math.pi*0.5
		if 'gain' in list(keys.keys()):
			self.Gain = keys['gain']
		else:
			print("WARNING! No gain given, using default gain = "+str(self.Gain))


		self.Q=math.sqrt(2.0)*0.5
		if 'Q' in list(keys.keys()):
			self.Q = keys['Q']
		else:
			print("WARNING! No Q give, using default Q = "+str(self.Q))


		self.fc=0
		if 'fc' in list(keys.keys()):
			self.fc = keys['fc']
		else:
			raise NameError("Missing fc!")

		
		
		self.cCoreID = Circuit.cCore.Add_SKLP(self.machine.cCoreID,
			c_double(self.fc), c_double(self.Q), c_double(self.Gain))

		self.SetInputs(**keys)

	def Initialize (self):
		pass
	def Update (self):
		pass



## \brief Active High Pass Filter circuit.
#
# \image html ActiveHighPass.png "schema"
# Takes a signal in and passes it through a High pass filter using the Sallen-Key topology
#
# \b Initialisation \b parameters:
# 	- \a gain =  Integer  How much gain the signal will recive 
# 	- \a Q = the Q value of the filter
#	- \a fc = the frequency cut off for the circuit
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- signal =  incoming signal
#
# \b Output \b channels:
# 	- \a out =\f$ \frac{\omega ^2 _c \cdot x(t) - \frac {y \cdot (t-2dt) - 2 \cdot y \cdot (t-dt)}{dt^2} + \frac{\omega ^2 _c}{2 \cdot Q \cdot dt} y \cdot (t-2dt)  }{ \frac{1}{dt^2} + \frac{\omega ^2 _c}{2 \cdot Q \cdot dt} + \omega ^2 _c  }\f$
#		where \f$ x \f$ is the input signal,  \f$ \omega_{c} = 2 \pi f_c \f$ is the cut off pulse \f$ Q \f$  is the quality factor and \f$ dt \f$ is the timestep.
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='SKHP', name='filter', fc=50, pushed='True')
# machine.AddCircuit(type='SKHP', name='filter', gain=10, Q=2, fc=50)
# \endcode
#
class SKHP(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("signal")
		self.AddOutput("out")


		self.Gain=math.pi*0.5
		if 'gain' in list(keys.keys()):
			self.Gain = keys['gain']
		else:
			print("WARNING! No gain given, using default gain = "+str(self.Gain))


		self.Q=math.sqrt(2.0)*0.5
		if 'Q' in list(keys.keys()):
			self.Q = keys['Q']
		else:
			print("WARNING! No Q give, using default Q = "+str(self.Q))


		self.Fcutoff=0
		if 'fc' in list(keys.keys()):
			self.fc = keys['fc']
		else:
			raise NameError("Missing fc!")

		self.cCoreID = Circuit.cCore.Add_SKHP(self.machine.cCoreID,
			c_double(self.fc), c_double(self.Q), c_double(self.Gain))

		
	def Initialize (self):
		pass
		
	def Update (self):
		pass

## \brief Active Band Pass Filter  circuit.
#
# \image html ActiveHighPass.png "schema"
# Takes a signal in and passes it through a Band pass filter using the Sallen-Key topology
#
# \b Initialisation \b parameters:
# 	- \a gain = output gain
#	- \a fc = the central frequency
#	- \a band = The band of frequncies that will be filtered.
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- \a signal = incoming signal
#
# \b Output \b channels:
# 	- \a out =\f$ G\frac{band \cdot dt\cdot(x(t) - x(t-2dt)) + band \cdot dt \cdot (2 \cdot y \cdot (t-dt) - y \cdot (t-2 \cdot dt)) }{ 1 + band \cdot dt + \omega ^2 _c } \f$
#   where \f$ x \f$ is the input signal, \f$ y \f$ is the input signal,  \f$ \omega_{c} = 2 \pi f_c \f$ is the cut off pulse \f$ Q \f$  is the quality factor and \f$ dt \f$ is the timestep.
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='SKBP', name='filter', fc=50, band=5, pushed='True')
# machine.AddCircuit(type='SKBP', name='filter', gain=10, fc=50, band=5, pushed='True')
# \endcode
#
class SKBP(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("signal")
		self.AddOutput("out")


		self.Gain=math.pi*0.5
		if 'gain' in list(keys.keys()):
			self.Gain = keys['gain']
		else:
			print("WARNING! No gain given, using default gain = "+str(self.Gain))

		self.fc=0
		if 'fc' in list(keys.keys()):
			self.fc = keys['fc']
		else:
			raise NameError("Missing fc!")

		self.band=0
		if 'band' in list(keys.keys()):
			self.band = keys['band']
		else:
			raise NameError("Missing band!")

		self.cCoreID = Circuit.cCore.Add_SKBP(self.machine.cCoreID,
			c_double(self.fc), c_double(self.band), c_double(self.Gain))


	def Initialize (self):
		pass

	def Update (self):
		pass


## \brief RC low-pass filter circuit.
#
# \image html PassiveLowPass.png "schema"
# Pass a signal through a series of \a order RC low pass filters with transfer function:... .
#
# \b Initialisation \b parameters:
#	- \a fc = the frequency cut off for the circuit
#	- \a order = the order of the filter
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels: 
# 	- \a signal = Incoming signal
#
# \b Output \b channels:
# 	- \a out = Filtered signal
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='RCLP', name='lp', fc=150, pushed='True')
# machine.AddCircuit(type='RCLP', name='lp', order=2, fc=50)
# \endcode
#
class RCLP(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("signal")
		self.AddOutput("out")


		self.fc=0

		if 'fc' in list(keys.keys()):
			self.fc = keys['fc']
		else:
			raise NameError("Missing fc!")

		self.Order=1
		if 'order' in list(keys.keys()):
			self.Order = keys['order']
		else:
			print("WARNING! Filter order not specified, using default order = "+str(self.Order))

		self.cCoreID = Circuit.cCore.Add_RCLP(self.machine.cCoreID,
			c_double(self.fc), self.Order)
		
	def Initialize (self):
		pass
	
	def Update (self):
		pass

## \brief RC high-pass filter circuit.
#
#
# \image html PassiveHighPass.png "schema"
# Pass a signal through a series of \a order RC high pass filters with transfer function:... .
#
# \b Initialisation \b parameters:
#	- \a fc = the frequency cut off for the circuit
#	- \a order = the order of the filter
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- \a signal = incoming signal
#
# \b Output \b channels:
# 	- \a out = Filtered signal
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='RCHP', name='hp', fc=50, pushed='True')
# machine.AddCircuit(type='RCHP', name='hp', order=2, Q=2, fc=50)
# \endcode
#
class RCHP(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("signal")
		self.AddOutput("out")


		self.fc=0
		if 'fc' in list(keys.keys()):
			self.fc = keys['fc']
		else:
			raise NameError("Missing fc!")


		self.Order=1
		if 'order' in list(keys.keys()):
			self.Order = keys['order']
		else:
			print("WARNING! No order given, using default order = "+str(self.Order))

		self.cCoreID = Circuit.cCore.Add_RCHP(self.machine.cCoreID,
			c_double(self.fc), self.Order)
		
	def Initialize (self):
		pass
		
	def Update (self):
		pass

