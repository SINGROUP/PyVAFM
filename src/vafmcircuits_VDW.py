from vafmbase import Circuit
import math
from ctypes import c_double
import ctypes


## \breif Van Der Walls force circuit.
# \image html VDW.png "schema"
#
# 
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels: 
# 	- \a gamma  = tip angle
#	- \a hamaker =  Hamaker constant
#	- \a radius = Tip Radius
#	- \a offset = tip offset
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

class VDW(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		if 'gamma' in keys.keys():
			alpha = keys['alpha']
			print "alpha = " +str(alpha)
		else:
			raise NameError("No alpha entered ")


		if 'hamaker' in keys.keys():
			hamaker = keys['hamaker']
			print "hamaker = " +str(hamaker)
		else:
			raise NameError("No hamaker entered ")


		if 'radius' in keys.keys():
			radius = keys['radius']
			print "radius = " +str(radius)
		else:
			raise NameError("No radius entered ")			


		if 'offset' in keys.keys():
			offset = keys['offset']
			print "offset = " +str(offset)
		else:
			raise NameError("No radius entered ")			

		
		self.AddInput("ztip")
		self.AddOutput("fz")


		Circuit.cCore.Add_VDW.argtypes = [
		ctypes.c_int, #Core Id
		ctypes.c_double, #alpha
		ctypes.c_double, #hamaker
		ctypes.c_double, #radius
		ctypes.c_double] #offset

		self.cCoreID = Circuit.cCore.Add_VDW(self.machine.cCoreID,alpha,hamaker,radius,offset)

		
		
		self.SetInputs(**keys)

	def Initialize (self):
		
		pass
		
		
		
		
	def Update (self):
		pass