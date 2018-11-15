from vafmbase import Circuit
import math
import ctypes

## \package vafmcircuits_STM
# This file contains the Scanning Tunneling Microscope circuit.
#


## \brief STM circuit.
#
# \image html STM.png "schema"
# Takes in a charge density and outputs current
# 
#
# \b Initialisation \b parameters:
# - pushed = True|False  push the output buffer immediately if True
# - WorkFunction = float Workfunction of the tip (Default value = 4eV).
# - WaveFunctionOverlap = float Wavefunction overlap of the tip and the sample (Default Value = 2 Angstrom). 
#
# \b Input \b channels:
# - \a Density 
#
# \b Output \b channels:
# - \a Current =  C \Delta S^2 k^2 n^2 
#
# 
# \b Example:
# \code{.py}
# machine.AddCircuit(type='STM',name='STM', pushed=True)
# \endcode
#

class STM(Circuit):


	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		if 'WorkFunction' in keys.keys():
			self.WF= keys['WorkFunction']
		else:
			print "WARNING: Using default workfunction of 4 eV"
			self.WF=4

		if 'WaveFunctionOverlap' in keys.keys():
			self.WaveFunctionOverlap= keys['WaveFunctionOverlap']
		else:
			print "WARNING: Using default Wave Function Overlap of 2 Angstrom"
			self.WaveFunctionOverlap=2


		self.cCoreID = Circuit.cCore.Add_STM(machine.cCoreID, ctypes.c_double(self.WF), ctypes.c_double(self.WaveFunctionOverlap) )


		self.AddInput("Density")
		self.AddOutput("Current")
		
		self.SetInputs(**keys)			

	def Initialize (self):
		pass


	def Update (self):
		pass
	

