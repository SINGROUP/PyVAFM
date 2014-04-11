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
# 	- \a gamma  = tip angle
#	- \a hamaker =  Hamaker constant
#	- \a radius = Tip Radius
#	- \a offset = tip offset
#
# \b Input \b channels: 
#	- \a ztip = z pos of tip
# \b Output \b channels: 
#	- \a fz = force 
#
#\b Examples:
# \code{.py}
#	machine.AddCircuit(type='VDW', name='VDW', gamma=0.28658 ,hamaker=39.6e-20 ,radius=3.9487, offset=0 , pushed=True)
# \endcode
#

class VDW(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		if 'gamma' in keys.keys():
			gamma = keys['gamma']
			print "gamma = " +str(gamma)
		else:
			raise NameError("No gamma entered ")


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
		ctypes.c_double, #gamma
		ctypes.c_double, #hamaker
		ctypes.c_double, #radius
		ctypes.c_double] #offset

		self.cCoreID = Circuit.cCore.Add_VDW(self.machine.cCoreID,gamma,hamaker,radius,offset)

		
		
		self.SetInputs(**keys)

	def Initialize (self):
		
		pass
			
		
	def Update (self):
		pass


class VDWtorn(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )


		if 'A1' in keys.keys():
			A1 = keys['A1']
			print "A1 = " +str(A1)
		else:
			raise NameError("No A1 entered ")

		if 'A2' in keys.keys():
			A2 = keys['A2']
			print "A2 = " +str(A2)
		else:
			raise NameError("No A2 entered ")

		if 'A3' in keys.keys():
			A3 = keys['A3']
			print "A3 = " +str(A3)
		else:
			raise NameError("No A3 entered ")			

		if 'A4' in keys.keys():
			A4 = keys['A4']
			print "A4 = " +str(A4)
		else:
			raise NameError("No A4 entered ")	

		if 'A5' in keys.keys():
			A5 = keys['A5']
			print "A5 = " +str(A5)
		else:
			raise NameError("No A5 entered ")	

		if 'tipoffset' in keys.keys():
			tipoffset = keys['tipoffset']
			print "tipoffset = " +str(tipoffset)
		else:
			raise NameError("No tipoffset entered ")	


		self.AddInput("ztip")
		self.AddOutput("fz")
		self.AddOutput("debug1")
		self.AddOutput("debug2")

		Circuit.cCore.Add_VDWtorn.argtypes = [
		ctypes.c_int, #Core Id
		ctypes.c_double, #A1
		ctypes.c_double, #A2
		ctypes.c_double, #A3
		ctypes.c_double, #A4
		ctypes.c_double, #A5
		ctypes.c_double] #tipoffset


		self.cCoreID = Circuit.cCore.Add_VDWtorn(self.machine.cCoreID,A1,A2,A3,A4,A5,tipoffset)
		
		self.SetInputs(**keys)

	def Initialize (self):
		
		pass
				
		
	def Update (self):
		pass		