# -*- coding:utf-8 -*-


## \package vafmcircuits_Cantilever
# This file contains the cantilever circuit

import numpy
import math
from vafmbase import Circuit
import ctypes


class Cantilever(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )
		
		if 'Q' in keys.keys():
			Q = keys['Q']
			print "Q = " +str(Q)
		else:
			raise NameError("No Q entered ")

		if 'k' in keys.keys():
			k = keys['k']
			print "k = "+str(k)
		else:
			raise NameError("No k entered ")

		if 'M' in keys.keys():
			M = keys['M']
			print "M = "+str(M)
		else:
			M = 0

		if 'f0' in keys.keys():
			F = keys['f0']
			print "f0 = "+str(F)
		else:
			raise NameError("No F entered ")
		
		startingz = 0
		if 'startingz' in keys.keys():
			startingz = keys['startingz']
			print "startingz = "+str(startingz)
		else:
			print "PY WARNING: starting tip z not specified, assuming 0"

		
		self.AddInput("holderz")
		self.AddInput("fz")
		self.AddInput("exciter")

		self.AddOutput("ztip")
		self.AddOutput("zabs")
		self.AddOutput("vz")

		self.cCoreID = Circuit.cCore.Add_Cantilever(self.machine.cCoreID,        #CAREFUL HERE!
			c_double(Q),c_double(k),c_double(M),c_double(F), c_double(startingz), c_double(0.0) )

		self.SetInputs(**keys);



class AdvancedCantilever(Circuit):
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )



		if 'NumberOfModesV' in keys.keys():
			NumberOfModesV = keys['NumberOfModesV']
			print "Number of Vertical Modes = " +str(NumberOfModesV)
		else:
			raise NameError("No NumberOfModesV entered ")

		if 'NumberOfModesL' in keys.keys():
			NumberOfModesL = keys['NumberOfModesL']
			print "Number of Lateral Modes = " +str(NumberOfModesL)
		else:
			raise NameError("No NumberOfModesL entered ")


		self.AddInput("exciterz")
		self.AddInput("excitery")
		self.AddInput("positionx")
		self.AddInput("positiony")
		self.AddInput("positionz")

		self.AddInput("Record")
		self.AddInput("Holderx")
		self.AddInput("Holdery")
		self.AddInput("Holderz")

		self.AddInput("ForceV")
		self.AddInput("ForceL")
		
		self.AddOutput("zPos")
		self.AddOutput("yPos")

		self.AddOutput("xABSv")
		self.AddOutput("yABSv")
		self.AddOutput("zABSv")

		self.AddOutput("xABSl")
		self.AddOutput("yABSl")
		self.AddOutput("zABSl")

		for i in range(1 ,NumberOfModesV+1):
			self.AddOutput("vV" + str(i) )
			self.AddOutput("zV" + str(i) )

		for i in range(1 ,NumberOfModesL+1):
			self.AddOutput("vL" + str(i) )
			self.AddOutput("yL" + str(i) )



		self.cCoreID = Circuit.cCore.Add_AdvancedCantilever(self.machine.cCoreID, NumberOfModesV,NumberOfModesL)

		self.SetInputs(**keys);


	def AddK(self, *args):
		Circuit.cCore.AddK.argtypes = [ctypes.POINTER(ctypes.c_double)]
		k=[]
		for i in args:
			k.append(i)
		karray = (ctypes.c_double * len(k))(*k)
		self.cCoreID = Circuit.cCore.AddK(karray)

	def AddQ(self, *args):
		Circuit.cCore.AddQ.argtypes = [ctypes.POINTER(ctypes.c_double)]
		Q=[]
		for i in args:
			Q.append(i)
		Qarray = (ctypes.c_double * len(Q))(*Q)
		self.cCoreID = Circuit.cCore.AddQ(Qarray)

	def AddM(self, *args):
		Circuit.cCore.AddM.argtypes = [ctypes.POINTER(ctypes.c_double)]
		M=[]
		for i in args:
			M.append(i)
		Marray = (ctypes.c_double * len(M))(*M)
		self.cCoreID = Circuit.cCore.AddM(Marray)

	def Addf0(self, *args):
		Circuit.cCore.AddF.argtypes = [ctypes.POINTER(ctypes.c_double)]
		f=[]
		for i in args:
			f.append(i)
		farray = (ctypes.c_double * len(f))(*f)
		self.cCoreID = Circuit.cCore.AddF(farray)

	def StartingPos(self, *args):
		Circuit.cCore.StartingPoint.argtypes = [ctypes.POINTER(ctypes.c_double)]
		StartingPoint=[]
		for i in args:
			StartingPoint.append(i)
		StartingPointarray = (ctypes.c_double * len(StartingPoint))(*StartingPoint)
		self.cCoreID = Circuit.cCore.StartingPoint(StartingPointarray)