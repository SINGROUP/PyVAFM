from vafmbase import Circuit
import math

#from vafmcircuits import Machine

## \package vafmcircuits_FlipFlop
# This file contains the flip flop circuits.
#


## \breif SR Flip Flop circuit.
# \image html SRFlipFlop.png "schema"
#
# Truth Table for SR FLip FLop
#
# S 			|R  		    | Q 			 |  QBar 		  |  Action 
# ------------- | ------------- |  ------------- |  ------------- |  -------------
# 0  			| 0             |   Q		  	 |	Qbar 		  | Hold State
# 0			    | 1				| 	0			 |  1			  | Reset
# 1			    | 0				| 	1			 |  0			  | Set
# 1			    | 1				| 	X			 |  X			  | Not Alowed
# 
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels: 
# 	- \a S = set signal
#	- \a R = reset signal
#	- \a clock = Clock signal
#
# \b Output \b channels: 
#	- \a Q =  stored bit (0|1)
#	- \a Qbar =  opposite of the stored bit
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='SRFlipFlop', name='sr')
# \endcode
#
class SRFlipFlop(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("S")
		self.AddInput("R")
		self.AddInput("clock")

		self.AddOutput("Q")
		self.AddOutput("Qbar")
		self.AddOutput("front")
		
		self.cCoreID = Circuit.cCore.Add_SRFlipFLop(self.machine.cCoreID)
		
		self.SetInputs(**keys)



	def Initialize (self):

		pass




	def Update (self):
		pass


## \brief JK Flip Flop circuit.
# \image html JKFlipFlop.png
#
# Truth Table JK Flip FLop
#
# J 			|K  		    | Q 			 |  QBar 		  |  Action 
# ------------- | ------------- |  ------------- |  ------------- |  -------------
# 0  			| 0             |   Q		  	 |	Qbar 		  | Hold State
# 0			    | 1				| 	0			 |  1			  | Reset
# 1			    | 0				| 	1			 |  0			  | Set
# 1			    | 1				| 	QBar		 |  Q			  | Toggle
# 
#
# \b Initialisation \b parameters: 
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels: 
# 	- \a J = set signal
#	- \a K = reset signal
#	- \a clock = Clock signal
#
#
# \b Output \b channels: 
#	- \a Q =  stored bit (0|1)
#	- \a Qbar =  opposite of the stored bit
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='JKFlipFlop', name='jk')
# \endcode
#
class JKFlipFlop(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("J")
		self.AddInput("K")
		self.AddInput("clock")

		self.AddOutput("Q")
		self.AddOutput("Qbar")
		self.AddOutput("front")
		
		self.cCoreID = Circuit.cCore.Add_JKFlipFLop(self.machine.cCoreID)
		
		self.SetInputs(**keys)


	def Initialize (self):

		pass




	def Update (self):		
		pass


## D Flip Flop circuit.
# \image html DFlipFlop.png
# Truth Table D Flip Fop
#
# D 			|   Q 			 |  QBar 		  |  Action 
# ------------- |  ------------- |  ------------- |  -------------
# 0  			|   Q 		  	 |	Qbar 		  | No Change
# 1			    | 	1			 |  0			  | Set
# 
# 
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- \a D = Data Channel
#	- \a clock = Clock signal
#
# \b Output \b channels: 
#	- \a Q =  stored bit (0|1)
#	- \a Qbar =  opposite of the stored bit
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='DFlipFlop', name='D')
# \endcode
#
class DFlipFlop(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("D")
		self.AddInput("clock")

		self.AddOutput("Q")
		self.AddOutput("Qbar")
		self.Qprevious = 0

		self.cCoreID = Circuit.cCore.Add_DFlipFLop(self.machine.cCoreID)
		
		self.SetInputs(**keys)

	def Initialize (self):

		pass




	def Update (self):		
		pass



## DR Flip Flop circuit.
# \image html DRFlipFlop.png
# Truth Table DR Flip Flop
#
# D 			|   R 			 |   Q 			 |  QBar 		    |  Action 
# ------------- |  ------------- |  -------------|  -------------   | ------------- 
# 0  			|   0 		  	 |  Q 		  	 |	Qbar 		    | No Change
# 0			    | 	1			 | 	0			 |  1			    | Reset
# 1			    | 	0			 |  0			 |  0				| Set
# 1				|   1			 |  x 			 |  x   			| Not Alowed
# \b Initialisation \b parameters: 
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels: 
# 	- \a D = Data Channel
#	- \a R = Reset Channel
#	- \a clock = Clock signal
#
# \b Output \b channels: 
#	- \a Q =  stored bit (0|1)
#	- \a Qbar =  opposite of the stored bit
#
class DRFlipFlop(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("D")
		self.AddInput("R")
		self.AddInput("clock")

		self.AddOutput("Q")
		self.AddOutput("Qbar")
		self.AddOutput("front")
		
		self.cCoreID = Circuit.cCore.Add_DRFlipFLop(self.machine.cCoreID)
		
		self.SetInputs(**keys)

	def Initialize (self):
		pass

	def Update (self):
		pass
