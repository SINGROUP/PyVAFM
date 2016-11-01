# -*- coding:utf-8 -*-

import numpy
import math
from vafmbase import Circuit
import ctypes
import tools


from numpy import *
from scipy.interpolate import griddata
import sys
import tools

## \package vafmcircuits_Cantilever
# This file contains the cantilever circuit

## \brief Simple cantilever circuit.
#	
# \image html cantilever.png "schema"
# 
# Simple cantilever capable of simulating 1 vertical mode.
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True.
# 	- \a startingz = The distance from equilibrium the cantilever will be placed at the start of the simulation.
# 	- \a Q = The Q factor of the cantilever.
# 	- \a k = spring constant of the cantilever.
# 	- \a f0 = Eigenfrequency of the cantilever.
#
# \b Input \b channels:
# 	- \a holderz =  Position of the cantilever holder in the z direction
# 	- \a fz = Force on the cantilever
# 	- \a exciter = excitation force for the cantilever
#
# \b Output \b channels:
# 	- \a ztip = vertical position of the tip
# 	- \a zabs = absoloute vertical position of the tip
# 	- \a vz = Vertical speed of the tip
#
#\b Examples:
# \code{.py}
#	canti = machine.AddCircuit(type='Cantilever',name='canti', startingz=0.5, Q=10000, k=167.0, f0=f0, pushed=True)
# \endcode
#
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
			ctypes.c_double(Q),ctypes.c_double(k),ctypes.c_double(M),
			ctypes.c_double(F),ctypes.c_double(startingz),ctypes.c_double(0.0) )

		self.SetInputs(**keys);


## \brief Advanced cantilever circuit.
#	
# \image html advcanti.png "schema"
# 
# Advanced cantilever capable of simulating infinite vertical mode and lateral modes.
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True.
# 	- \a NumberOfModesV = The number of vertical modes the cantilever has.
# 	- \a NumberOfModesL = The number of lateral modes the cantilever has.
#
# \b Initialisation \b commands:
#	- \a .AddMode(Vertical=True|False, k=float, Q=float, M=float, f0 =float)- this is how you add a mode to the cantilever, Vertical = True means a vertical mode, Vertical = False is a lateral.
#						k is the spring constant for that mode, Q is the Q factor, M is the mass although if tis is not included the simulation will calculate a mass for you and f0 is the eigenfrequency of the mode.
# 	- \a .StartingPos(x,y,z) - Assigns the starting position from equilibrium for the cantilever. 
#	- \a .CantileverReady() - use this command after you are done setting up the cantilever.
#
# \b Input \b channels:
# 	- \a exciterz =  cantilever exciter for the vertical direction.
# 	- \a excitery = cantilever exciter for the lateral direction.
# 	- \a Holderx = Position of the cantilever holder in the x direction.
# 	- \a Holdery = Position of the cantilever holder in the y direction.
# 	- \a Holderz = Position of the cantilever holder in the z direction.
# 	- \a ForceV = Vertical force experinced by the cantilever.
# 	- \a ForceL = Lateral force experinced by the cantilever.
#
# \b Output \b channels:
# 	- \a zPos = vertical position of the tip.
# 	- \a yPos = Lateral positon of the tip.
# 	- \a xABS = absoloute x position of the tip.
# 	- \a yABS = absoloute y position of the tip.
# 	- \a zABS = absoloute z position of the tip.
# 	- \a vVx = Velocity of a vertical mode, replace x with the mode number for example vV1.
# 	- \a vLx = Velocity of a lateral mode, replace x with the mode number for example vV1.
# 	- \a zVx = Z position of a vertical mode, replace x with the mode number for example zV1.
# 	- \a YLx = Y position of a lateral mode, replace x with the mode number for example yV1.
#
#\b Examples:
# \code{.py}
#	canti = machine.AddCircuit(type='AdvancedCantilever',name='canti',NumberOfModesV=2,NumberOfModesL=0, pushed=True)
#	canti.AddMode(Vertical=True, k = 1, Q=100, M=1, f0 =1)
#	canti.AddMode(Vertical=True, k = 1, Q=100, M=1, f0 =1)
#	canti.AddMode(Vertical=False, k = 1, Q=100, M=1, f0 =1)
#	canti.StartingPos(0,3,5)
#	canti.CantileverReady()
# \endcode
#

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

		self.NumberOfModesL = NumberOfModesL
		self.NumberOfModesV = NumberOfModesV


		for i in range(1 ,NumberOfModesV+2):
			self.AddOutput("vV" + str(i) ) #5 to #5 + NumberOfModesV

		for i in range(1 ,NumberOfModesV+2):			
			self.AddOutput("zV" + str(i) ) #5 + NumberOfModesV  to #5 + NumberOfModesV*2

		for i in range(1 ,NumberOfModesL+2):
			self.AddOutput("vL" + str(i) ) #5 + NumberOfModesV*2 to #5 + NumberOfModesV*2 + NumberOfModesL
			
		for i in range(1 ,NumberOfModesL+2):			
			self.AddOutput("yL" + str(i) ) #5 + NumberOfModesV*2 + NumberOfModesL + #5 + NumberOfModesV*2 + NumberOfModesL*2
		#required vars
		self.vertical = True

		self.counterV=0
		self.counterL=0

		self.Kv=[]
		self.Kl=[]

		self.Qv=[]
		self.Ql=[]

		self.Mv=[]
		self.Ml=[]

		self.fov=[]
		self.fol=[]


		
		self.cCoreID = Circuit.cCore.Add_AdvancedCantilever(self.machine.cCoreID, NumberOfModesV,NumberOfModesL)
		self.SetInputs(**keys);

	def StartingPos(self, *args):
		if (len(args) != 3):
			raise NameError("Incorrect number of starting values entered")


		Circuit.cCore.StartingPoint.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
		StartingPoint=[]
		for i in args:
			StartingPoint.append(i)
		StartingPointarray = (ctypes.c_double * len(StartingPoint))(*StartingPoint)
		Circuit.cCore.StartingPoint(self.cCoreID,StartingPointarray)


	def AddMode(self, **kw):

		if 'k' not in kw.keys():
			raise NameError("Missing k from AddMode")

		if 'Q' not in kw.keys():
			raise NameError("Missing Q from AddMode")

		if 'M' not in kw.keys():
			kw["M"]=0		
			print "Warning Missing Mass will caulcuate from omega and k"

		if 'f0' not in kw.keys():
			raise NameError("Missing f0 from AddMode")


		if kw["Vertical"] == True : 
			if "k" in kw.keys(): self.Kv.append(float(kw["k"]))
			if "Q" in kw.keys(): self.Qv.append(float(kw["Q"]))
			if "M" in kw.keys(): self.Mv.append(float(kw["M"]))
			if "f0" in kw.keys(): self.fov.append(float(kw["f0"]))
			self.counterV =+ 1

		if kw["Vertical"] == False : 
			if "k" in kw.keys(): self.Kl.append(float(kw["k"]))
			if "Q" in kw.keys(): self.Ql.append(float(kw["Q"]))
			if "M" in kw.keys(): self.Ml.append(float(kw["M"]))
			if "f0" in kw.keys(): self.fol.append(float(kw["f0"]))
			self.counterL =+ 1


	def CantileverReady(self):
		#combine arrays
		k = self.Kv + self.Kl
		Q = self.Qv + self.Ql
		M = self.Mv + self.Ml
		f = self.fov + self.fol

		if self.counterV > self.NumberOfModesV:
			raise NameError("Incorrect number of vertical modes added check initialisation parameters")

		if self.counterL > self.NumberOfModesL:
			raise NameError("Incorrect number of lateral modes added check initialisation parameters")

		karray = (ctypes.c_double * len(k))(*k)
		Circuit.cCore.AddK(self.cCoreID, karray)

		Qarray = (ctypes.c_double * len(Q))(*Q)
		Circuit.cCore.AddQ(self.cCoreID, Qarray)

		Marray = (ctypes.c_double * len(M))(*M)
		Circuit.cCore.AddM(self.cCoreID, Marray)

		farray = (ctypes.c_double * len(f))(*f)

		Circuit.cCore.AddF(self.cCoreID,farray)		






class AnalyticalCantilever(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )


		A = 0.13
		f0 = 1.553e6
		K = 130


		if 'filename' in keys.keys():
			FILENAME = keys["filename"]
		else:
			raise NameError("Missing filename")

		if 'NumberOfPoints' in keys.keys():
			NumberOfPoints = keys["NumberOfPoints"]
		else:
			raise NameError("Missing NumberOfPoints")

		if 'K' in keys.keys():
			K = keys["K"]
		else:
			raise NameError("Missing K")


		if 'A' in keys.keys():
			A = keys["A"]
		else:
			raise NameError("Missing A")

		if 'f0' in keys.keys():
			f0 = keys["f0"]
		else:
			raise NameError("Missing f0")



		res = [51,51,201]
		if 'res' in keys.keys():
			res = keys["res"]

		step = []
		if 'step' in keys.keys():
			step = keys["step"]
		else:
			raise NameError("Missing step")

		NumberOfUnitCells = [1,1,1]
		if 'NumberOfFFCells' in keys.keys():
			NumberOfUnitCells = keys["NumberOfFFCells"]


		convertion=1
		if 'convertion' in keys.keys():
			convertion = keys["convertion"]


		zHeight = None
		if 'zHeight' in keys.keys():
			zHeight = keys["zHeight"]


		OutputFile = ""
		if 'OutputFile' in keys.keys():
			OutputFile = keys["OutputFile"]
		else:
			raise NameError("Missing OutputFile")


		OscRes=100
		if 'OscRes' in keys.keys():
			OscRes = keys["OscRes"]

		if 'TipPos' in keys.keys():
			TipPos = keys["TipPos"]



		arrayx = linspace(TipPos[0],  (step[0]*NumberOfPoints[0]*NumberOfUnitCells[0])+TipPos[0],res[0])
		arrayy = linspace(TipPos[1],  (step[1]*NumberOfPoints[1]*NumberOfUnitCells[1])+TipPos[1],res[1])
		arrayz = linspace(A, (step[2]*NumberOfPoints[2]*NumberOfUnitCells[2])+TipPos[2],res[2])



		if 'ScanType' in keys.keys():
			ScanType = keys["ScanType"]
			if ScanType != "Vertical":
				if ScanType != "Lateral":
					print "ERROR: Scan type can only be Vertical or Lateral"
					sys.exit()

		if zHeight != None and ScanType == "Lateral": 
			arrayz=[zHeight]

		if ScanType == "Vertical":
			arrayx=[TipPos[0]]
			arrayy=[TipPos[1]]

		if 'MinMaxz' in keys.keys():
			MinMaxz = keys["MinMaxz"]
			arrayz = linspace(MinMaxz[0], MinMaxz[1],res[2])

		force=[]



		
		FF = open(FILENAME,'r')
		Data = [[[0 for k in xrange( int (NumberOfPoints[2]) ) ] for j in xrange( int (NumberOfPoints[1]) )] for i in xrange(int (NumberOfPoints[0]) )]

		for line in FF:	
			i = int(line.split()[0])-1
			j = int(line.split()[1])-1
			k = int(line.split()[2])-1
			Data[i][j][k]=float(line.split()[3])*convertion


		counter = 0
		linecounter =0
		xpos = 0
		ypos = 0
		Resultsx = []
		Resultsy = []
		Resultsz = []
		Resultsdf = []
		ForceTest=[]


		for ypos in arrayy:
			linecounter+=1
			print "Running line number "+str(linecounter)
			
			for xpos in arrayx:
				
				for z in arrayz:
					#Solve the integral from 0 to 2pi
					Integral = 0
					size = OscRes
					x = linspace(0, 2*pi, size)


					#Find x_0
					pos = float(z+A*cos(x[0]))
					Force= tools.interpolate(Data,step,xpos,ypos,pos)
					#Force= tools.interpolate(Data,[0.705,0.705,0.1],xpos,ypos,pos)
					
					Integral += cos(x[0])*Force


					#x_1 tp x _ size-1
					for i in range(1,size -1):

						pos = float(z+A*cos(x[i]))
						Force= tools.interpolate(Data,step,xpos,ypos,pos)
						#Force= tools.interpolate(Data,[0.705,0.705,0.1],xpos,ypos,pos)

						if i%2 == 0: #Is even
							Integral += 2* cos(x[i])*Force

						if i%2 != 0: #Is odd
							Integral += 4* cos(x[i])*Force	
					

					#Find x_size_n
					pos = float(z+A*cos(x[size-1]))
					Force= tools.interpolate(Data,step,xpos,ypos,pos)
					#Force= tools.interpolate(Data,[0.705,0.705,0.1],xpos,ypos,pos)
					Integral += cos(x[size-1])*Force



					Integral = Integral * ((x[0]-x[size-1])/ (len(x)-1)  )/3

					FreqShift =Integral * f0 / (2*pi * K*A) 
					Resultsx.append(xpos)
					Resultsy.append(ypos)
					Resultsz.append(z)
					Resultsdf.append(FreqShift)



		W = open(OutputFile, 'w')
		counter = 0
		for i in range(0,len(Resultsx)):
			W.write(str(Resultsx[i]) +" "+str(Resultsy[i]) + " "+str(Resultsz[i]) + " " + str(Resultsdf[i]) +"\n")
			oldy= Resultsy[i]
			counter +=1
		W.close()

		self.SetInputs(**keys);
