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
#	- \a fcut = the frequency cut off for the circuit
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
# machine.AddCircuit(type='SKLP', name='filter', fcut=150)
# machine.AddCircuit(type='SKLP', name='filter', gain=10, Q=2, fcut=50, pushed='True')
# \endcode
#
class SKLP(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("signal")
		self.AddOutput("out")


		self.Gain=math.pi*0.5
		if 'gain' in keys.keys():
			self.Gain = keys['gain']
		else:
			print "WARNING! No gain given, using default gain = "+str(self.Gain)


		self.Q=math.sqrt(2.0)*0.5
		if 'Q' in keys.keys():
			self.Q = keys['Q']
		else:
			print "WARNING! No Q give, using default Q = "+str(self.Q)


		self.fc=0
		if 'fcut' in keys.keys():
			self.fc = keys['fcut']
		else:
			raise NameError("Missing fcut!")

		
		
		self.cCoreID = Circuit.cCore.Add_SKLP(self.machine.cCoreID,
			c_double(self.fc), c_double(self.Q), c_double(self.Gain))

		self.SetInputs(**keys)

		"""
		self.wc = 2* math.pi * self.fc * machine.dt
		self.gamma = self.wc/(2*self.Q)

		self.wc=self.wc*self.wc
		self.alpha=1/(1 + self.gamma + self.wc)

		self.y=0
		self.yo=0
		self.yoo=0
		self.x = 0
		self.y = 0
		"""

	def Initialize (self):
		
		pass
		
		
		
		
	def Update (self):
		pass
		"""
		self.x = self.I["signal"].value 

		self.y = self.Gain*self.wc*self.x + (2.0*self.yo-self.yoo) + self.gamma*self.yoo 
		self.y = self.y * self.alpha
		self.O["out"].value=self.y


		self.yoo=self.yo
		self.yo=self.y
		"""



## \brief Active High Pass Filter circuit.
#
# \image html ActiveHighPass.png "schema"
# Takes a signal in and passes it through a High pass filter using the Sallen-Key topology
#
# \b Initialisation \b parameters:
# 	- \a gain =  Integer  How much gain the signal will recive 
# 	- \a Q = the Q value of the filter
#	- \a fcut = the frequency cut off for the circuit
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
# machine.AddCircuit(type='SKHP', name='filter', fcut=50, pushed='True')
# machine.AddCircuit(type='SKHP', name='filter', gain=10, Q=2, fcut=50)
# \endcode
#
class SKHP(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("signal")
		self.AddOutput("out")


		self.Gain=math.pi*0.5
		if 'gain' in keys.keys():
			self.Gain = keys['gain']
		else:
			print "WARNING! No gain given, using default gain = "+str(self.Gain)


		self.Q=math.sqrt(2.0)*0.5
		if 'Q' in keys.keys():
			self.Q = keys['Q']
		else:
			print "WARNING! No Q give, using default Q = "+str(self.Q)


		self.Fcutoff=0
		if 'fcut' in keys.keys():
			self.fc = keys['fcut']
		else:
			raise NameError("Missing fcut!")

		self.cCoreID = Circuit.cCore.Add_SKHP(self.machine.cCoreID,
			c_double(self.fc), c_double(self.Q), c_double(self.Gain))

		

		"""
		self.wc = 2* math.pi * self.fc * machine.dt
		self.gamma = self.wc/(2*self.Q)

		self.alpha=1/(1 + self.gamma + self.wc*self.wc)

		self.y=0
		self.yo=0
		self.yoo=0
		self.x = 0
		self.xo=0
		self.xoo=0
		"""
	
	def Initialize (self):
		
		pass
		
		
		
		
	def Update (self):
		pass
		"""
		self.x = self.I["signal"].value 
		self.y = (2*self.yo-self.yoo) + self.gamma*self.yoo + self.Gain*(self.xoo-2.0*self.xo+self.x);
		self.y=self.y*self.alpha

		self.O["out"].value=self.y

		self.yoo=self.yo
		self.yo=self.y

		self.xoo=self.xo
		self.xo=self.x
		"""

## \brief Active Band Pass Filter  circuit.
#
# \image html ActiveHighPass.png "schema"
# Takes a signal in and passes it through a Band pass filter using the Sallen-Key topology
#
# \b Initialisation \b parameters:
# 	- \a gain =  Integer  How much gain the signal will recive 
#	- \a fc = the frequency cut off for the circuit
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
		if 'gain' in keys.keys():
			self.Gain = keys['gain']
		else:
			print "WARNING! No gain given, using default gain = "+str(self.Gain)

		self.fc=0
		if 'fc' in keys.keys():
			self.fc = keys['fc']
		else:
			raise NameError("Missing fc!")

		self.band=0
		if 'band' in keys.keys():
			self.band = keys['band']
		else:
			raise NameError("Missing band!")

		self.cCoreID = Circuit.cCore.Add_SKBP(self.machine.cCoreID,
			c_double(self.fc), c_double(self.band), c_double(self.Gain))

		"""
		self.gamma = self.band
		self.wc = self.fc
		self.gamma = self.wc/self.gamma

		self.wc = 2 * math.pi * self.wc * machine.dt
		self.gamma = self.wc /(2*self.gamma)

		self.alpha = 1/(1 + self.gamma + self.wc*self.wc)

		self.y=0
		self.yo=0
		self.yoo=0
		self.x = 0
		self.xo=0
		self.xoo=0
		"""
		
	def Initialize (self):
		pass
		
		
		
		
	def Update (self):
		pass
		"""
		self.x = self.I["signal"].value 

		self.y = self.Gain*self.gamma*(self.x-self.xoo) + self.gamma*self.yoo + (2.0*self.yo-self.yoo)

		self.y=self.y*self.alpha

		self.O["out"].value=self.y

		self.yoo=self.yo
		self.yo=self.y

		self.xoo=self.xo
		self.xo=self.x
		"""

## \brief RC low-pass filter circuit.
#
# \image html PassiveLowPass.png "schema"
# Pass a signal through a series of \a order RC low pass filters with transfer function:... .
#
# \b Initialisation \b parameters:
#	- \a fcut = the frequency cut off for the circuit
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
# machine.AddCircuit(type='RCLP', name='lp', fcut=150, pushed='True')
# machine.AddCircuit(type='RCLP', name='lp', order=2, fcut=50)
# \endcode
#
class RCLP(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("signal")
		self.AddOutput("out")


		self.fc=0
		if 'fc' in keys.keys():
			self.fc = keys['fc']
		else:
			raise NameError("Missing fcut!")


		self.Order=1
		if 'order' in keys.keys():
			self.Order = keys['order']
		else:
			print "WARNING! No order given, using default order = "+str(self.Order)

		self.fc = 2*math.pi*self.fc # fc -> wc
		self.a = 2*machine.dt*self.fc # this is 2dt wc
		self.a = self.a/(1+self.a) # this is 2dt wc/(1+2dt wc)
		#self.a = machine.dt/(machine.dt+(1.0/self.fc)) # this is 2dt wc
		
		self.y  = [0] * (self.Order +1) #this is the output at time t+dt of each filter, y[0] is the incoming signal
		self.yo = [0] * (self.Order +1) #this is the output at time t of each filter		
		self.yoo= [0] * (self.Order +1) #this is the output at time t-dt of each filter		
		#print self.folds

		self.cCoreID = Circuit.cCore.Add_RCLP(self.machine.cCoreID,
			c_double(self.fc), self.Order)
		
	def Initialize (self):
		
		pass
		
		
	
	def Update (self):
		
		
		self.y[0] = self.I["signal"].value 
		
		for i in range(self.Order):
			self.y[i+1] = self.a*self.y[i] + (1-self.a)*self.yoo[i+1]
		
		self.O["out"].value= self.y[self.Order]

		#collect old values
		for i in range(self.Order+1):
			self.yoo[i] = self.yo[i]
			self.yo[i] = self.y[i]

## \brief RC high-pass filter circuit.
#
#
# \image html PassiveHighPass.png "schema"
# Pass a signal through a series of \a order RC high pass filters with transfer function:... .
#
# \b Initialisation \b parameters:
#	- \a fcut = the frequency cut off for the circuit
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
# machine.AddCircuit(type='RCHP', name='hp', fcut=50, pushed='True')
# machine.AddCircuit(type='RCHP', name='hp', order=2, Q=2, fcut=50)
# \endcode
#
class RCHP(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("signal")
		self.AddOutput("out")


		self.fc=0
		if 'fc' in keys.keys():
			self.fc = keys['fc']
		else:
			raise NameError("Missing fcut!")


		self.Order=1
		if 'order' in keys.keys():
			self.Order = keys['order']
		else:
			print "WARNING! No order given, using default order = "+str(self.Order)

		#self.fc = 1/(2*math.pi * self.fc)
		#self.a = self.fc/(machine.dt +self.fc) #what was this?
		
		self.fc = 2*math.pi*self.fc # fc -> wc
		self.a = 2*machine.dt*self.fc # this is (2dt wc)
		self.a = 1.0/(1+self.a) # this is 2dt wc/(1+2dt wc)

		self.y  = [0] * (self.Order +1) #this is the output at time t+dt of each filter, y[0] is the incoming signal
		self.yo = [0] * (self.Order +1) #this is the output at time t of each filter	
		self.yoo = [0] * (self.Order +1) #this is the output at time t-dt of each filter	

		self.cCoreID = Circuit.cCore.Add_RCHP(self.machine.cCoreID,
			c_double(self.fc), self.Order)
		
	def Initialize (self):
		
		pass
		
	def Update (self):

		
		self.y[0] = self.I["signal"].value 

		for i in range(self.Order):
			
			self.y[i+1] = (self.y[i]-self.yoo[i]+ self.yoo[i+1])*self.a
			#print i+1, self.y[i+1],self.yo[i+1],self.yoo[i+1],"inputs:",self.y[i],self.yoo[i],self.a
			#time.sleep(0.01)

		for i in range (0, self.Order + 1):
			self.yoo[i] = self.yo[i]
			self.yo[i] = self.y[i]
		
		self.O["out"].value= self.y[self.Order]
		
