from vafmbase import Circuit
import math
from ctypes import c_double

## \package vafmcircuits_math
# This file contains the basic arithmetic operator circuits.
#
#

## \brief Arithmetic sum circuit.
#
# \image html opAdd.png "schema"
# Sums up the input signals 'in#' and outputs the result in 'out'.
# The amount of input signals is set with the 'factors=#' argument when
# the circuit is created.
#
# \b Initialisation \b parameters:
# 	- \a factors = # number of input channels
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- \a in1, \a in2, ..., \a inx =  incoming signals
#
#
# \b Output \b channels: 
# 	- \a out = \f$\sum_i^{factors} in_i\f$
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='opAdd', name='adder')
# machine.AddCircuit(type='opAdd', name='summer', factors=4)
# machine.AddCircuit(type='opAdd', name='summer', in2=3.5)
# \endcode
#
class opAdd(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		## Amount of input channels to sum. Default is 2.
		self.factors = 2
		
		#check if the amount of factors was given	
		if 'factors' in keys.keys():
			self.factors = keys['factors']
		
		
		#create input channels
		for i in range(self.factors):
			self.AddInput("in"+str(i+1))
		
		#create output channels
		self.AddOutput("out")
		
		self.cCoreID = Circuit.cCore.Add_Math(self.machine.cCoreID,"opADD",self.factors)

		
		
		self.SetInputs(**keys)

	def Initialize (self):
		
		pass
		
		
		
		
	def Update (self):
		pass

## \brief Arithmetic subtraction circuit.
#
# Outputs the difference between two input signals 'in#' in the output 'out'.
#
# \image html opSub.png "schema"
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
#	- \a in1, \a in2  = input signals
#
# \b Output \b channels: 
# 	- \a out = \f$ in_1 - in_2 \f$ 
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='opSub', name='minus')
# machine.AddCircuit(type='opSub', name='minus', in2=3.5)
# \endcode
#
class opSub(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		#create input channels
		self.AddInput("in1")
                self.AddInput("in2")
		
		#create output channels
		self.AddOutput("out")
		
		self.cCoreID = Circuit.cCore.Add_Math(self.machine.cCoreID,"opSUB",2)
		
		self.SetInputs(**keys)

	def Initialize (self):
		
		pass
		
        
	def Update (self):
		pass

## \brief Arithmetic multiplier circuit.
#
# \image html opMul.png "schema"
# Multiplies the input signals 'in#' and outputs the result in 'out'.
# The amount of input signals is set with the 'factors=#' argument when
# the circuit is created.
#
# \b Initialisation \b parameters:
# 	- \a factors = # number of input channels
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- \a in1, \a in2, ..., \a inx  incoming signals
#
# \b Output \b channels:
# 	-  \a out = \f$ \prod_i^{factors} in_i \f$
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='opMul', name='mul')
# machine.AddCircuit(type='opMul', name='mul', factors=4)
# machine.AddCircuit(type='opMul', name='mul', in2=0.4)
# \endcode
#
class opMul(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		#check if the amount of factors was given	
		self.factors = 2
		if 'factors' in keys.keys():
			self.factors = int(keys['factors'])
		
		
		#create input channels
		for i in range(self.factors):
			self.AddInput("in"+str(i+1))
		
		#create output channels
		self.AddOutput("out")
		
		self.cCoreID = Circuit.cCore.Add_Math(self.machine.cCoreID,"opMUL",self.factors)
		
		self.SetInputs(**keys)
		

	def Initialize (self):
		pass
		
		
	def Update (self):
		pass



## \brief Arithmetic division circuit.
#
# Outputs the ratio between two input signals 'in#' in the output 'out'.
#
# \image html opDiv.png "schema"
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- \a in1, \a in2 =  input signals
#
# \b Output \b channels:
# 	- \a out = \f$ in_1 / in_2 \f$
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='opDiv', name='div')
# machine.AddCircuit(type='opDiv', name='div', in2=0.5)
# \endcode
#
class opDiv(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		#create input channels
		self.AddInput("in1")
		self.AddInput("in2")
		
		#create output channels
		self.AddOutput("out")
		
		self.cCoreID = Circuit.cCore.Add_Math(self.machine.cCoreID,"opDIV",2)
		
		self.SetInputs(**keys)

	def Initialize (self):
		
		pass
		
        
	def Update (self):
		pass

## \brief Arithmetic linear-combo circuit.
#
# \image html opLinC.png "schema"
# Computes the linear combination of the input signals 'ina#' and 'inb#',
# and outputs the result in 'out'.
# The amount of input signals is set with the 'factors=#' argument when
# the circuit is created.
#
# \b Initialisation \b parameters:
# 	- \a factors = # number of factors
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- \a ina1, \a ina2, ..., \a inax = incoming signals
# 	- \a inb1, \a inb2, ..., \a inbx = incoming signals
#
# \b Output \b channels:
# 	- \a out = \f$ \sum_i^{factors} ina_i\times inb_i \f$
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='opLinC', name='combo')
# machine.AddCircuit(type='opLinC', name='combo', factors=4)
# machine.AddCircuit(type='opLinC', name='combo', inb1=5.2)
# \endcode
#
class opLinC(Circuit):

	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		#check if the amount of factors was given	
		self.factors = 2
		if 'factors' in keys.keys():
			self.factors = keys['factors']
		
		
		#create input channels
		for i in range(self.factors):
			self.AddInput("ina"+str(i+1))
			self.AddInput("inb"+str(i+1))
		
		#create output channels
		self.AddOutput("out")
		
		self.cCoreID = Circuit.cCore.Add_Math(self.machine.cCoreID,"opLINC",self.factors*2)
		
		self.SetInputs(**keys)
		

	def Initialize (self):
		pass
		
	def Update (self):
		pass


## \brief Absolute value operator circuit.
#
# \image html opAbs.png "schema"
# Takes in an inpute and returns the Absolute vcalue of it
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- \a signal =  incoming signal
#
# \b Output \b channels:
# 	- \a out = \f$|in|\f$
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='opAbs', name='abs')
# \endcode
#
class opAbs(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )


		self.AddInput("signal")
		
		#create output channels
		self.AddOutput("out")
		
		
		self.cCoreID = Circuit.cCore.Add_Math(self.machine.cCoreID,"opABS",1)
		
		self.SetInputs(**keys)

	def Initialize (self):
		pass
	
	def Update (self):
		pass


## Power operator circuit.
## \brief Power value circuit.
#
# Takes in an inpute and returns the result raised to a given power
#
# \image html opPow.png "schema"
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#	- \a power = integer The value the function result will be raised by
#
# \b Input \b channels:
# 	- \a signal = incoming signal
#
# \b Output \b channels:
# 	- \a out =  \f$ signal^{power} \f$
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='opPow', name='pow', power=3.45)
# \endcode
#
class opPow(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )

		if 'power' in keys.keys():
			self.power = keys['power']
		else:
			raise SyntaxError("ERROR! power not specified.")

		self.AddInput("signal")
		
		#create output channels
		self.AddOutput("out")
		
		self.cCoreID = Circuit.cCore.Add_Math(self.machine.cCoreID,"opPOW",2)
		
		self.SetInputs(**keys)

	def Initialize (self):
		pass
	
	def Update (self):
		pass



## \brief Sin operator circuit.
#
# \image html opSin.png "schema"
# Computes the sine of an input signal
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- \a signal =  incoming signal
#
# \b Output \b channels:
# 	- \a out = \f$sin(in)\f$
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='opSin', name='sin')
# \endcode
#
class opSin(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )


		self.AddInput("signal")
		
		#create output channels
		self.AddOutput("out")
		
		self.cCoreID = Circuit.cCore.Add_Math(self.machine.cCoreID,"opSIN",1)
		
		self.SetInputs(**keys)

	def Initialize (self):
		pass
	
	def Update (self):
		pass

## \brief Cos operator circuit.
#
# \image html opSin.png "schema"
# Computes the cosine of an input signal
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- \a signal =  incoming signal
#
# \b Output \b channels:
# 	- \a out = \f$cos(in)\f$
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='opCos', name='cos')
# \endcode
#
class opCos(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )


		self.AddInput("signal")
		
		#create output channels
		self.AddOutput("out")
		
		self.cCoreID = Circuit.cCore.Add_Math(self.machine.cCoreID,"opCOS",1)
		
		self.SetInputs(**keys)

	def Initialize (self):
		
		pass
	
	def Update (self):
		pass

## \brief Perlin Noise circuit.
#
# \image html Perlin.png "schema"
# Outputs perlin noise
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True.
# 	- \a octaves = Number of octaves to combine.
#	- \a amp  = amplitude, the difference between the lowest noise value and the largest.
#	- \a persist = Persitance of the perlin noise (how noisy the end result will be).
#	- \a period  = period of the noise wave.
#
# \b Input \b channels:
# 	- \a signal =  incoming signal
#
# \b Output \b channels:
# 	- \a out = signal plus noise
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='opCos', name='cos')
# \endcode
#
class Perlin(Circuit):
	
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )

		
		if "octaves" in keys.keys():
			self.octaves = int(keys["octaves"])
		else:
			raise ValueError("ERROR: number of octaves not specified!")

		self.amp = 1
		if "amp" in keys.keys():
			self.amp = float(keys["amp"])
		else:
			print "WARNING: Perlin amplitude not specified, assuming 1."
		
		if "persist" in keys.keys():
			self.persist = float(keys["persist"])
		else:
			raise ValueError("ERROR: persistance not specified!")

		if "period" in keys.keys():
			self.period = float(keys["period"])
		else:
			raise ValueError("ERROR: period not specified!")

		
		self.AddInput("signal")
		
		#create output channels
		self.AddOutput("out")
		
		self.cCoreID = Circuit.cCore.Add_Perlin(self.machine.cCoreID,
			c_double(self.amp),c_double(self.persist),self.octaves, c_double(self.period))
		
		self.SetInputs(**keys)

	def Initialize (self):
		
		pass
	
	def Update (self):
		pass

