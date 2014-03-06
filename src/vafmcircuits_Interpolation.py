# -*- coding:utf-8 -*-
## \package vafmcircuits_Interpolation
# This file contains the interpolation for the force field.
# \file vafmcircuits_Interpolation.py
# This file contains the interpolation for the force field.

import numpy
import math
from vafmbase import Circuit
from scipy.interpolate import LinearNDInterpolator
import ctypes

## \brief Tri-linear interpolation circuit.
#
# This is the circuit that calculates the interpolation of the provided force field.
# The force field must be in the following format, but plese note that the interpolation
# circuit is capable of taking any number of dimensions and components in,
# but for a case where there is an unequal amount of dimensions and components the
# unused components column must be filled with zeros.
# Except in the case of 3 dimensions and 1 component, this can be left as it is.
# Examples of how the force fields must be formated is shown below.: \n
# <pre> x y z Fx Fy Fz or x y z F or x y z Fx 0 0 or x y Fx 0 <pre>
#
# - \b Initialisation \b parameters:
# - \a Filename = Filename of the force field input file.
# - \a Dimensions = Number of dimensons in the force field.
# - \a Components = Number of components of force in the force field.
#
# - \b Input \b channels:
# - \a coord : this is the coordiante to calcualte the interpolation.
#
# - \b Output \b channels:
# - \a Fx: The interpolated forces where x is the component for example F1 would be first first component.
#
# \b Example:
# \code
# inter = machine.AddCircuit(type='Interpolate',name='inter', Filename = 'Force.dat', Dimensions = 3, Components = 3 ,pushed=True)
# \endcode
#

class i3Dlin(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		if 'components' in keys.keys():
			self.components = keys['components']
			print "components = " +str(self.components)
		else:
			raise NameError("No components entered ")
		
		self.npts = None; self.nptsSET = False
		self.step = None; self.stepSET = False
		self.pbc = None; self.pbcSET = False
		self.data = None

		self.AddInput("x")
		self.AddInput("y")
		self.AddInput("z")

		for i in range(0,self.components):
			self.AddOutput("F"+str(i+1))

		
		self.cCoreID = Circuit.cCore.Add_i3Dlin(self.machine.cCoreID, self.components)
		
		Circuit.cCore.i3Dlin_step.argtypes = [
			ctypes.c_int, #Core Id
			ctypes.c_double, #xstep
			ctypes.c_double, #ystep
			ctypes.c_double] #zstep
		Circuit.cCore.i3Dlin_npts.restype =  ctypes.POINTER(ctypes.POINTER(ctypes.c_double))
		
		self.SetInputs(**keys)

	def Configure(self, **keys):
		
		#check for npoints
		if 'npoints' in keys.keys():
			if len(keys['npoints']) != 3:
				raise ValueError("ERROR! the number of points is not a triplet!")
			else:
				self.npts = [int(n) for n in keys['npoints']]
				print "i3Dlin: npoints",self.npts
				self.nptsSET = True
				#send the changes to cCore
				self.data = Circuit.cCore.i3Dlin_npts(self.cCoreID, self.npts[0], self.npts[1], self.npts[2])
				#print self.data[0][0]
				
		#check for steps
		if 'steps' in keys.keys():
			if len(keys['steps']) != 3:
				raise ValueError("ERROR! the grid steps is not a triplet!")
			else:
				self.step = keys['steps']
				print "i3Dlin: steps",self.step
				self.stepSET = True
				#call a cCore function to save the values
				Circuit.cCore.i3Dlin_step(self.cCoreID, self.step[0], self.step[1], self.step[2])
			
		#check for pbc
		if 'pbc' in keys.keys():
			if len(keys['pbc']) != 3:
				raise ValueError("ERROR! the PBC is not a triplet!")
			else:
				self.pbc = [0,0,0]
				for i in xrange(len(keys['pbc'])):
					if keys['pbc'][i] == True:
						self.pbc[i] = 1
					else:
						self.pbc[i] = 0
				#print "PBC ",self.pbc
				Circuit.cCore.i3Dlin_pbc(self.cCoreID, self.pbc[0], self.pbc[1], self.pbc[2])
				self.pbcSET = True
	
	def ReadData(self,filename):
		
		if self.nptsSET == False:
			raise ValueError("ERROR! The amount of grid points along each axis was not yet specified!")
		if self.stepSET == False:
			raise ValueError("ERROR! The grid step sizes were not yet specified!")
					
		fsize = self.npts[0]*self.npts[1]*self.npts[2]
		yzsize = self.npts[1]*self.npts[2]
		zsize = self.npts[2]
		
		
		f = open(filename, "r")
		for line in f:
			words = line.split()
			i = int(words[0])-1
			j = int(words[1])-1
			k = int(words[2])-1
			index = i*yzsize + j*zsize + k
			for c in xrange(self.components): #convert the components to float
				words[c+3] = ctypes.c_double(float(words[c+3]))
				self.data[c][index] = words[c+3]
		
		f.close()




class i1Dlin(Circuit):
    
    
	def __init__(self, machine, name, **keys):        
			
		super(self.__class__, self).__init__( machine, name )

		self.components = 0
		if 'comp' in keys.keys():
			self.components = int(keys['comp'])
			print "components = " +str(self.components)
		else:
			raise NameError("No components entered ")

		if 'step' in keys.keys():
			step = keys['step']
			print "step = " +str(step)
		else:
			raise NameError("No step entered ")
		
		
		if 'pbc' in keys.keys():
			if keys['pbc'] == True:
				pbc = 1
			else:
				pbc = 0
		else:
			raise NameError("No pbc entered ")


		self.AddInput("x")
		
		for i in range(0,self.components):
			self.AddOutput("F"+str(i+1))
		
		Circuit.cCore.Add_i1Dlin.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.c_double,ctypes.c_int]
		self.cCoreID = Circuit.cCore.Add_i1Dlin(machine.cCoreID
			, ctypes.c_int(self.components)
			, ctypes.c_double(step)
			, ctypes.c_int(pbc))

		self.SetInputs(**keys)

	def SetData(self, datapoints):
		
		npts = len(datapoints)
		if(npts < 2):
			raise ValueError("ERROR: there are less than 2 points in the field!")
		
		#(int index, int c, double* data, int npts)
		Circuit.cCore.i1Dlin_SetData.argtypes = [ctypes.c_int,ctypes.c_int,
			ctypes.POINTER(ctypes.c_double),ctypes.c_int]
		
		if self.components > 1:
			for c in range(self.components):
				
				lst = [p[c] for p in datapoints]
				#print lst
				test_arr = (ctypes.c_double * npts)(*lst)
				
				Circuit.cCore.i1Dlin_SetData(self.cCoreID, c,test_arr,npts)
		else:
			test_arr = (ctypes.c_double * npts)(*datapoints)
			Circuit.cCore.i1Dlin_SetData(self.cCoreID, 0,test_arr,npts)





