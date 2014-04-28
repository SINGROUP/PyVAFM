## \package vafmcircuits_Logic
# This file contains the basic logic operator circuits.

from vafmbase import Circuit
import math

## \brief Not Gate
# \image html Not.png "schema"
#
# Truth Table for a Not Gate
#
# signal        |out
# ------------- | -------------
# 1                         | 0
# 0                         | 1                                
#
# - \b Initialisation \b parameters:
# 	- \a pushed = True|False push the output buffer immediately if True
#
# - \b Input \b channels:
#	- \a signal = incoming signal
#
# - \b Output \b channels:
# 	- \a out = \! \a signal
#
# \b Example:
# \code
# machine.AddCircuit(type='NOT', name='not', pushed=True)
# \endcode
#
class NOT(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("signal")
		self.AddOutput("out")

		self.cCoreID = Circuit.cCore.Add_Logic(self.machine.cCoreID,"opNOT",1)

		self.SetInputs(**keys)

	def Initialize (self):
		pass

	def Update (self):
		pass


## And Gate
# \image html And.png "schema"
#
# Truth table for an And Gate
# in1           |in2            |out
# ------------- | ------------- | -------------
# 0                         | 0 | 0
# 0                         | 1                                | 0
# 1                         | 0                                | 0
# 1                         | 1                                | 1
#
#
# - \b Initialisation \b parameters:
# 	- \a pushed = True|False push the output buffer immediately if True
# 	- \a factors = number of input channels. Default is 2.
#
# - \b Input \b channels:
# 	- \a in1, \a in2, ..., \a inx = incoming signals
#
# - \b Output \b channels:\n
# 	- \a out = \a in_1 \f$ \land \f$ \a in_2 \f$ \land\f$ ... \f$ \land \f$ \a in_x \f$
#
# \b Example:
# \code
# machine.AddCircuit(type='AND', name='andgate', factors=4)
# machine.AddCircuit(type='AND', name='andgate', pushed=True)
# \endcode
#
class AND(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		# ## Amount of input channels to put in the AND. Default is 2.
		self.factors = 2

		#check if the amount of factors was given        
		if 'factors' in keys.keys():
			self.factors = keys['factors']
		#print ' factors: '+str(self.factors)
		
		#create input channels
		for i in range(self.factors):
			self.AddInput("in"+str(i+1))
		
		self.AddOutput("out")

		self.cCoreID = Circuit.cCore.Add_Logic(self.machine.cCoreID,"opAND",self.factors)

		self.SetInputs(**keys)

	def Initialize (self):
		pass        

	def Update (self):
		pass


class NAND(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )


		
		#create input channels
		self.AddInput("in1")
		self.AddInput("in2")
		
		self.AddOutput("out")

		self.cCoreID = Circuit.cCore.Add_Logic(self.machine.cCoreID,"opNAND",2)

		self.SetInputs(**keys)

	def Initialize (self):
		pass        

	def Update (self):
		pass


## Or Gate
# \image html OrGate.png "schema"
#
# Truth table for a Or Gate
# in1           |in2            |out
# ------------- | ------------- | -------------
# 0             | 0 | 0
# 0             | 1 | 1
# 1             | 0 | 1
# 1             | 1 | 1
#
# - \b Initialisation \b parameters:
#         - \a pushed = True|False push the output buffer immediately if True.
#         - \a factors = number of input channels. Default is 2.
#
# - \b Input \b channels:
#         - \a in1, \a in2, ... = incoming signal
#
# - \b Output \b channels:\n
# 	- \a out = \a in_1 \f$ \lor \f$ \a in_2 \f$ \lor \f$ ... \f$ \lor \f$ \a in_x \f$
#
# \b Example:
# \code
# machine.AddCircuit(type='OR', name='or', factors=3)
# machine.AddCircuit(type='OR', name='or', pushed=True)
# \endcode
#
class OR(Circuit):

	def __init__(self, machine, name, **keys):
	
		super(self.__class__, self).__init__( machine, name )

		# ## Amount of input channels to put in the AND. Default is 2.
		self.factors = 2


		#check if the amount of factors was given        
		if 'factors' in keys.keys():
			self.factors = keys['factors']
		#print ' factors: '+str(self.factors)
		
		#create input channels
		for i in range(self.factors):
			self.AddInput("in"+str(i+1))

		self.AddOutput("out")

		self.cCoreID = Circuit.cCore.Add_Logic(self.machine.cCoreID,"opOR",self.factors)

		self.SetInputs(**keys)

		self.result = 0

	def Initialize (self):
		pass        

	def Update (self):
		pass             


## XOr Gate
# \image html XOrGate.png "schema"
#
# Truth table for a XOr Gate
# in1                |in2                |out
# ------------- | ------------- | -------------
# 0                         | 0 | 0
# 0                         | 1                                | 1
# 1                         | 0                                | 1
# 1                         | 1                                | 0
#
# - \b Initialisation \b parameters:
#         - \a pushed = True|False push the output buffer immediately if True.
#         - \a factors = number of input channels. Default is 2.
#
# - \b Input \b channels:
#         - \a in1, \a in2, ... = incoming signal
#
# - \b Output \b channels:\n
# 	- \a out = \a in_1 \f$ \oplus \f$ \a in_2 \f$ \oplus \f$ ... \f$ \oplus \f$ \a in_x \f$
#
# \b Example:
# \code
# machine.AddCircuit(type='XOR', name='xor', factors=3)
# machine.AddCircuit(type='XOR', name='xor', pushed=True)
# \endcode
#
class XOR(Circuit):

	def __init__(self, machine, name, **keys):
	
		super(self.__class__, self).__init__( machine, name )

		# ## Amount of input channels to put in the AND. Default is 2.
		self.factors = 2

		#check if the amount of factors was given        
		if 'factors' in keys.keys():
			self.factors = keys['factors']
		
		#create input channels
		for i in range(self.factors):
			self.AddInput("in"+str(i+1))
		
		self.AddOutput("out")

		self.cCoreID = Circuit.cCore.Add_Logic(self.machine.cCoreID,"opXOR",self.factors)

		self.SetInputs(**keys)

		self.result = 0


	def Initialize (self):
		pass        

	def Update (self):
		pass


## NOR Gate
# \image html NOrGate.png "schema"
#
# Truth table for a NOr Gate
# in1                |in2                |out
# ------------- | ------------- | -------------
# 0                         | 0 | 1
# 0                         | 1                                | 0
# 1                         | 0                                | 0
# 1                         | 1                                | 0
#
# - \b Initialisation \b parameters:
# 	- \a pushed = True|False push the output buffer immediately if True.
# 	- \a factors = number of input channels. Default is 2.
#
# - \b Input \b channels:
# 	- \a in1, \a in2 = incoming signals
#
# - \b Output \b channels:
# 	- \a out = ! (\in1 \f$ \lor \f$ \a in2 ... \f$ \lor \f$ \a inx )
#
# \b Example:
# \code
# machine.AddCircuit(type='NOR', name='nor', factors=4)
# machine.AddCircuit(type='NOR', name='nor', pushed=True)
# \endcode
#
class NOR(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		# ## Amount of input channels to put in the AND. Default is 2.
		self.factors = 2

		#check if the amount of factors was given        
		if 'factors' in keys.keys():
			self.factors = keys['factors']
		#print ' factors: '+str(self.factors)
		
		#create input channels
		for i in range(self.factors):
			self.AddInput("in"+str(i+1))

		self.AddOutput("out")

		self.cCoreID = Circuit.cCore.Add_Logic(self.machine.cCoreID,"opNOR",self.factors)

		self.SetInputs(**keys)


	def Initialize (self):
		pass        

	def Update (self):
		pass
