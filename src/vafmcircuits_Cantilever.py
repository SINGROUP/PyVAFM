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

		self.NumberOfModesL = NumberOfModesL
		self.NumberOfModesV = NumberOfModesV	


		self.AddInput("exciterz") #0
		self.AddInput("excitery") #1

		self.AddInput("Holderx") #2
		self.AddInput("Holdery") #3
		self.AddInput("Holderz") #4

		self.AddInput("ForceV") #5
		self.AddInput("ForceL") #6
		
		self.AddOutput("zPos") #0
		self.AddOutput("yPos") #1

		self.AddOutput("xABS") #2
		self.AddOutput("yABS") #3
		self.AddOutput("zABS") #4


		for i in range(1 ,NumberOfModesV+2):
			self.AddOutput("vV" + str(i) ) #5 to #5 + NumberOfModesV

		for i in range(1 ,NumberOfModesV+2):			
			self.AddOutput("zV" + str(i) ) #5 + NumberOfModesV  to #5 + NumberOfModesV*2

		for i in range(1 ,NumberOfModesL+2):
			self.AddOutput("vL" + str(i) ) #5 + NumberOfModesV*2 to #5 + NumberOfModesV*2 + NumberOfModesL
			
		for i in range(1 ,NumberOfModesL+2):			
			self.AddOutput("yL" + str(i) ) #5 + NumberOfModesV*2 + NumberOfModesL + #5 + NumberOfModesV*2 + NumberOfModesL*2



		self.cCoreID = Circuit.cCore.Add_AdvancedCantilever(self.machine.cCoreID, NumberOfModesV,NumberOfModesL)

		self.SetInputs(**keys);


	def AddK(self, *args):
		if (len(args) != self.NumberOfModesL + self.NumberOfModesV):
			raise NameError("Incorrect number of spring constants entered")

		Circuit.cCore.AddK.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
		k=[]
		for i in args:
			k.append(i)
		karray = (ctypes.c_double * len(k))(*k)
		Circuit.cCore.AddK(self.cCoreID, karray)

	def AddQ(self, *args):
		if (len(args) != self.NumberOfModesL + self.NumberOfModesV):
			raise NameError("Incorrect number of Q factors constants entered")

		Circuit.cCore.AddQ.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
		Q=[]
		for i in args:
			Q.append(i)
		Qarray = (ctypes.c_double * len(Q))(*Q)
		Circuit.cCore.AddQ(self.cCoreID, Qarray)

	def AddM(self, *args):
		if (len(args) == 0):
			print "WARNING: Calculating masses from omega and k"

		if (len(args) != self.NumberOfModesL + self.NumberOfModesV and len(args) != 0) :
			raise NameError("Incorrect number of masses entered")		

		#TODO Check if no mass is given and if not calculate and put into the array
		Circuit.cCore.AddM.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
		M=[]
		for i in args:
			M.append(i)
		Marray = (ctypes.c_double * len(M))(*M)
		Circuit.cCore.AddM(self.cCoreID, Marray)

	def Addf0(self, *args):
		if (len(args) != self.NumberOfModesL + self.NumberOfModesV):
			raise NameError("Incorrect number of eigenfrequencies entered")

		Circuit.cCore.AddF.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
		f=[]
		for i in args:
			f.append(i)
		farray = (ctypes.c_double * len(f))(*f)
		Circuit.cCore.AddF(self.cCoreID,farray)

	def StartingPos(self, *args):
		if (len(args) != 3):
			raise NameError("Incorrect number of starting values entered")


		Circuit.cCore.StartingPoint.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
		StartingPoint=[]
		for i in args:
			StartingPoint.append(i)
		StartingPointarray = (ctypes.c_double * len(StartingPoint))(*StartingPoint)
		Circuit.cCore.StartingPoint(self.cCoreID,StartingPointarray)