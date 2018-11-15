from vafmbase import Circuit
import math
import ctypes

## \brief Van Der Waals force circuit.
# \image html VDW.png "schema"
#
# 
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
# 	- \a alpha  = tip angle
#	- \a hamaker =  Hamaker constant
#	- \a radius = Tip Radius
#	- \a offset = tip offset
#
# \b Input \b channels: 
#	- \a ztip = z posisiton of the tip
#
# \b Output \b channels: 
#	- \a fz = force 
#
#\b Examples:
# \code{.py}
#	machine.AddCircuit(type='VDW', name='vdw', alpha=0.28658 ,hamaker=39.6e-20 ,radius=3.9487, offset=0 , pushed=True)
# \endcode
#
class VDW(Circuit):


	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		if 'alpha' in list(keys.keys()):
			alpha = keys['alpha']
			print("alpha = " +str(alpha))
		else:
			raise NameError("No alpha entered ")


		if 'hamaker' in list(keys.keys()):
			hamaker = keys['hamaker']
			print("hamaker = " +str(hamaker))
		else:
			raise NameError("No hamaker entered ")


		if 'radius' in list(keys.keys()):
			radius = keys['radius']
			print("radius = " +str(radius))
		else:
			raise NameError("No radius entered ")			


		if 'offset' in list(keys.keys()):
			offset = keys['offset']
			print("offset = " +str(offset))
		else:
			raise NameError("No offset entered ")	

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


class VDWtorn(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )


		if 'A1' in list(keys.keys()):
			A1 = keys['A1']
			print("A1 = " +str(A1))
		else:
			raise NameError("No A1 entered ")

		if 'A2' in list(keys.keys()):
			A2 = keys['A2']
			print("A2 = " +str(A2))
		else:
			raise NameError("No A2 entered ")

		if 'A3' in list(keys.keys()):
			A3 = keys['A3']
			print("A3 = " +str(A3))
		else:
			raise NameError("No A3 entered ")			

		if 'A4' in list(keys.keys()):
			A4 = keys['A4']
			print("A4 = " +str(A4))
		else:
			raise NameError("No A4 entered ")	

		if 'A5' in list(keys.keys()):
			A5 = keys['A5']
			print("A5 = " +str(A5))
		else:
			raise NameError("No A5 entered ")	

		if 'A6' in list(keys.keys()):
			A6 = keys['A6']
			print("A6 = " +str(A6))
		else:
			A6=0

		if 'tipoffset' in list(keys.keys()):
			tipoffset = keys['tipoffset']
			print("tipoffset = " +str(tipoffset))
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
		ctypes.c_double, #A6		
		ctypes.c_double] #tipoffset


		self.cCoreID = Circuit.cCore.Add_VDWtorn(self.machine.cCoreID,A1,A2,A3,A4,A5,A6,tipoffset)
		
		self.SetInputs(**keys)

	def Initialize (self):
		pass
				
		
	def Update (self):
		pass		




## \brief Lennard Jones Potential circuit.
# \image html LJ.png "schema"
#
# Produces a Lennard Jones potentinal with given paramaters
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
# 	- \a epsilon  = epsilon of the Lennard Jones potential
#	- \a sigma =  Sigma of the Lennard Jones potential
#
# \b Input \b channels: 
#	- \a ztip = z posisiton of the tip
#
# \b Output \b channels: 
#	- \a F = Total Potential Output
#	- \a Repulsive = Just the repuslive part of the Potential
#	- \a Attractive = Just the attractive part of the Potential
#
#\b Examples:
# \code{.py}
#	machine.AddCircuit(type='LJ', name='lj',epsilon=3.9487, sigma=1 , pushed=True)
# \endcode
#



class LJ(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )

		if 'epsilon' in list(keys.keys()):
			ep = keys['epsilon']
		else:
			raise NameError("No epsilon entered ")


		if 'sigma' in list(keys.keys()):
			sig = keys['sigma']
		else:
			raise NameError("No sigma entered ")


		self.AddInput("ztip")
		
		self.AddOutput("F")
		self.AddOutput("Repulsive")
		self.AddOutput("Attractive")


		Circuit.cCore.Add_LJ.argtypes = [
		ctypes.c_int, #owner
		ctypes.c_double, #ep
		ctypes.c_double] #sig

		self.cCoreID = Circuit.cCore.Add_LJ(self.machine.cCoreID,ep,sig)
		
		self.SetInputs(**keys)


	def Initialize (self):
		pass
				
		
	def Update (self):
		pass	