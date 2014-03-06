from vafmbase import Circuit
import math

## \package vafmcircuits_Comparison
# This file contains the comparison operator circuits.
#

## \brief Greater or equal to  circuit.
#
# \image html GreaterOrEqual.png "schema"
# Takes two signals in and if signal 1 is greater than or equal to signal 2 then output a 1
#
# \b Initialisation \b parameters:
# 	- \a pushed True|False
#
# \b Input \b channels:
# 	- \a in1 =  incoming signal 1
# 	- \a in2 =  incoming signal 2
#
# \b Output \b channels:
# 	- \a out = if \a in1 is \f$ \geq \f$ \a in2 then output 1
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='GreaterOrEqual', name='GreaterOrEqual',pushed = 'True')
# \endcode
#
class GreaterOrEqual(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("in1")
		self.AddInput("in2")

		self.AddOutput("out")

		self.cCoreID = Circuit.cCore.Add_Comparison(self.machine.cCoreID,"GreaterOrEqual",2)

		self.SetInputs(**keys)

	def Initialize (self):

		pass	

	def Update (self):
		result=0

		if self.I["in1"].value >= self.I["in2"].value :
			result=1
		self.O['out'].value = result

## \brief Less or equal to  circuit.
#
# \image html LessOrEqual.png "schema"
# Takes two signals in and if signal 1 is less than or equal to signal 2 then output a 1
#
# \b Initialisation \b parameters:
# 	- \a pushed True|False
#
# \b Input \b channels:
# 	- \a in1 =  incoming signal 1
# 	- \a in2 =  incoming signal 2
#
# \b Output \b channels:
# 	- \a out = if \a in1 is \f$ \leq \f$ \a in2 then output 1
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='LessOrEqual', name='LessOrEqual',pushed = 'True')
# \endcode
#
class LessOrEqual(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("in1")
		self.AddInput("in2")

		self.AddOutput("out")
		
		self.cCoreID = Circuit.cCore.Add_Comparison(self.machine.cCoreID,"LessOrEqual",2)

		self.SetInputs(**keys)

	def Initialize (self):

		pass	

	def Update (self):
		result=0

		if self.I["in1"].value <= self.I["in2"].value :
			result=1
		self.O['out'].value = result

## \brief equal to  circuit.
#
# \image html Equal.png "schema"
# Takes two signals in and if signal 1 is equal to signal 2 then output a 1
#
# \b Initialisation \b parameters:
# 	- \a pushed True|False
#
# \b Input \b channels:
# 	- \a in1 =  incoming signal 1
# 	- \a in2 =  incoming signal 2
#
# \b Output \b channels:
# 	- \a out = if \a in1 \f$ = \f$ \a in2 then output 1
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='Equal', name='Equal',pushed = 'True')
# \endcode
#
class Equal(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("in1")
		self.AddInput("in2")

		self.AddOutput("out")
		
		self.cCoreID = Circuit.cCore.Add_Comparison(self.machine.cCoreID,"Equal",2)
		
		self.SetInputs(**keys)

	def Initialize (self):

		pass	

	def Update (self):
		result=0

		if self.I["in1"].value == self.I["in2"].value :
			result=1
		self.O['out'].value = result
