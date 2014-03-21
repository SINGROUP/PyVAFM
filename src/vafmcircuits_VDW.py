from vafmbase import Circuit
import math
from ctypes import c_double
import ctypes

class VDW(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		if 'alpha' in keys.keys():
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