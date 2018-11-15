## \package vafmcircuits_control.py
# This file contains the controller circuits.
#

from vafmbase import Circuit
from vafmbase import ChannelType
from vafmbase import Channel
from ctypes import *

import math

class RSA(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("exciter")
		self.AddInput("eta")
		self.AddInput("mu")
		
		self.AddOutput("xcm")
		self.AddOutput("ycm")
		self.AddOutput("theta")
		self.AddOutput("x2")

		Circuit.cCore.RSA_SetMasses.argtypes = [c_int, c_double, c_double, c_double]
		Circuit.cCore.RSA_SetGammas.argtypes = [c_int, c_double, c_double, c_double]
		Circuit.cCore.RSA_SetPoints.argtypes = [c_int, c_double, c_double, c_double]
		Circuit.cCore.RSA_SetSprings.argtypes = [c_int, c_double, c_double, c_double]
		
		self.cCoreID = Circuit.cCore.Add_RSA(machine.cCoreID)
		
		self.masses = [1,1,1]
		if "masses" in list(keys.keys()):
			self.masses = keys["masses"]
			self._SetMasses()
		
		self.springs = [1,1,1]
		if "springs" in list(keys.keys()):
			self.springs = keys["springs"]
			self._SetSprings()
			
		self.gammas = [0.1,0.1,0.1]
		if "gammas" in list(keys.keys()):
			self.gammas = keys["gammas"]
			self._SetGammas()
			
		self.points = [1,1,-1]
		if "points" in list(keys.keys()):
			self.points = keys["points"]
			self._SetPoints()
		
		self.SetInputs(**keys)
		
		
	def Initialize (self):

		pass

	def _SetSprings(self):
		Circuit.cCore.RSA_SetSprings(self.cCoreID, self.springs[0], self.springs[1], self.springs[2])
	def SetSprings(self, k1,k1z,k2):
		self.springs = [k1,k1z,k2]
		self._SetSprings()
	
	def _SetPoints(self):
		Circuit.cCore.RSA_SetPoints(self.cCoreID, self.points[0], self.points[1], self.points[2])
	def SetPoints(self,springx,springy,forcep):
		self.points = [springx,springy,forcep]
		self._SetPoints()
		
	def _SetGammas(self):
		Circuit.cCore.RSA_SetGammas(self.cCoreID, self.gammas[0], self.gammas[1], self.gammas[2])
	def SetGammas(self,g1,g2,grot):
		self.gammas = [g1,g2,grot]
		self._SetGammas()
	
	def _SetMasses(self):
		Circuit.cCore.RSA_SetMasses(self.cCoreID, self.masses[0], self.masses[1], self.masses[2])
	def SetMasses(self,m1,m2,mi):
		self.masses = [m1,m2,mi]
		self._SetMasses()

	def Update (self):
		pass

