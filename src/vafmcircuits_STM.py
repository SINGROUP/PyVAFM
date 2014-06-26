from vafmbase import Circuit
import math
import ctypes

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


		self.cCoreID = Circuit.cCore.Add_STM(machine.cCoreID, c_double(self.WorkFunction), c_double(self.WaveFunctionOverlap) )


		self.AddInput("Density")
		self.AddOutput("Current")
		
		self.SetInputs(**keys)			

	def Initialize (self):
		pass


	def Update (self):
		pass
	

