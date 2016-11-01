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
import sys
import os
import glob
## \brief Tri-linear interpolation circuit.
#
# \image html i3dlin.png "schema"
#
# This is the circuit that calculates the interpolation of the provided force field.
# The force field must be in the following format, but plese note that the interpolation circuit is capable of taking any number of components in. 
#
# x y z F1 F2 F3 
#
# The force field must also use a constant step size for each dimenson, although the force field can be in any order. The x y and z must also be the index
# of the point eg: 1 1 1 , 1 1 2 , 1 1 3 etc. When you configure the circuit later on you set the steps size to whatever you want it to be.
#
# - \b Initialisation \b parameters:.
# 	- \a Components = Number of components of force in the force field.
# 	- \a pushed True|False
# - \b Initialisation \b commands:
#	- Configure(steps=array, npoints=integer, pbc=True|False, ForceMultipler=float)
#		- \a steps = step size of the force field must be specfied in this format [x,y,z]
#		- \a npoints = number of points in each dimension must be specfied in this format [xn,yn,zn]
#		- \a pbc = Perodic boundray conditions for each dimenson, must be specfied in this format [True|False,True|False,True|False]
#		- \a ForceMultipler = A global multipler for all the force field values, use this to change the units of the force field into what ever units are desired.
#	-  ReadData(filename = string)
#		- \a Filename is the force field being interpolated.
# - \b Input \b channels:
#	 - \a x : this is x the coordiante to calculate the interpolation.
#	 - \a y : this is y the coordiante to calculate the interpolation.
#	 - \a z : this is z the coordiante to calculate the interpolation.
# - \b Output \b channels:
# 	- \a Fn: The interpolated forces where n is the component for example F1 would be first first component.
#
# \b Example:
# \code
#	inter = machine.AddCircuit(type='i3Dlin',name='inter', components=1, pushed=True)
#	inter.Configure(steps=[0.805714285714286,0.805714285714286,0.1], npoints=[8,8,171])
#	inter.Configure(pbc=[True,True,False])
#	inter.Configure(ForceMultiplier=1e10)
#	inter.ReadData('NaClforces.dat')
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
				
				Circuit.cCore.i3Dlin_pbc(self.cCoreID, self.pbc[0], self.pbc[1], self.pbc[2])
				self.pbcSET = True

		if 'ForceMultiplier' in keys.keys():
			self.ForceMultiplier = keys['ForceMultiplier']
			print "ForceMultiplier = " +str(self.ForceMultiplier)
		else:
			self.ForceMultiplier = 1

	
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
				words[c+3] = ctypes.c_double(float(words[c+3]) * self.ForceMultiplier)
				self.data[c][index] = words[c+3]
		
		f.close()


## \brief linear interpolation circuit.
#
# \image html i1dlin.png "schema"
#
# This is the circuit that calculates the interpolation of the provided 1D force field.
# The force field must be in the following format, but plese note that the interpolation circuit is capable of taking any number of components in. 
#
# x F1
#
# The force field must also use a constant step size for each dimenson, although the force field can be in any order.
#
# - \b Initialisation \b parameters:.
# 	- \a Components = Number of components of force in the force field.
#	- \a step = step size for the force field.
# 	- \a pushed True|False = push the output buffer immediately if True.
#	- \a pbc True|False = perodic boundray conditions.
# - \b Initialisation \b commands:
#	- SetData(array) = arrays must be the set of forces you wish to interpolate over.
#
# - \b Input \b channels:
#	 - \a x : this is x the coordiante to calculate the interpolation.
# - \b Output \b channels:
# 	- \a Fn: The interpolated forces where n is the component for example F1 would be first first component.
#
# \b Example:
# \code
#	inter = machine.AddCircuit(type='i1Dlin',name='inter', comp=2, step=0.1, pbc=True, pushed=True)
#	forces = [[math.sin(2*math.pi*x/20),math.cos(2*2*math.pi*x/20)] for x in range(20)]
#	inter.SetData(forces)
# \endcode
#

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

		if 'ForceUnits' in keys.keys():
			self.ForceUnits=float(keys['ForceUnits'])
		else:
			self.ForceUnits= 1.0





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

		for i in range(0,len(datapoints)):
			datapoints[i] = datapoints[i]*self.ForceUnits

		if(npts < 2):
			raise ValueError("ERROR: there are less than 2 points in the field!")
		
		
		Circuit.cCore.i1Dlin_SetData.argtypes = [ctypes.c_int,ctypes.c_int,
			ctypes.POINTER(ctypes.c_double),ctypes.c_int]
		
		if self.components > 1:
			for c in range(self.components):
				
				lst = [p[c] for p in datapoints]
				
				test_arr = (ctypes.c_double * npts)(*lst)
				
				Circuit.cCore.i1Dlin_SetData(self.cCoreID, c,test_arr,npts)
		else:
			test_arr = (ctypes.c_double * npts)(*datapoints)
			Circuit.cCore.i1Dlin_SetData(self.cCoreID, 0,test_arr,npts)


## \brief Vasp quad-linear interpolation circuit.
#
# \image html i4dlin.png "schema"
#
# This is the circuit that calculates the interpolation of 4d PARCHG data that is outputted from VASP and is used for STM images.
#
# - \b Initialisation \b parameters:.
# 	- \a Components = Number of components of force in the force field.
# 	- \a pushed True|False
# - \b Initialisation \b commands:
#	 - \a BiasStep  = The stepsize of the bias between the VASP files.
#	 - \a StartingV = The starting value of the voltage.
#	 - \a ConfigureVASP 
#			-\a pbc = True|False True|False True|False The perodic boundary condition for x y and z.
# - \b Input \b channels:
#	 - \a x : this is x the coordiante to calculate the interpolation.
#	 - \a y : this is y the coordiante to calculate the interpolation.
#	 - \a z : this is z the coordiante to calculate the interpolation.
#	 - \a V : this ist he voltage of the STM.
# - \b Output \b channels:
# 	- \a F: The interpolated output.
#
# \b Example:
# \code
#	inter = machine.AddCircuit(type='i4Dlin',name='inter', components=1, pushed=True)
#	inter.BiasStep=0.5
#	inter.StartingV=1
#	inter.ConfigureVASP(pbc=[True,True,False,False])
#	inter.ReadVASPData("parchg.1.0")
# \endcode
#

class i4DlinVasp(Circuit):
    
    
	def __init__(self, machine, name, **keys):        
			
		super(self.__class__, self).__init__( machine, name )

		#Vasp files only have 1 component
		self.components = 1

		Circuit.cCore.Add_i4Dlin.argtypes = [ctypes.c_int,ctypes.c_int]
		self.cCoreID = Circuit.cCore.Add_i4Dlin(machine.cCoreID, self.components)
		self.BiasStep=0
		self.StartingV=-1
		self.pbcSET = False
		self.AddInput("x")
		self.AddInput("y")
		self.AddInput("z")
		self.AddInput("V")


		for i in range(0,self.components):
			self.AddOutput("F")

		self.SetInputs(**keys)

	def ConfigureVASP(self, **keys):
				#check for pbc
		if 'pbc' in keys.keys():
			if len(keys['pbc']) != 4:
				raise ValueError("ERROR! the PBC is not a triplet!")
			else:
				self.pbc = [0,0,0,0]
				for i in xrange(len(keys['pbc'])):
					if keys['pbc'][i] == True:
						self.pbc[i] = 1
					else:
						self.pbc[i] = 0
				
				Circuit.cCore.i4DLinPBC(self.cCoreID, self.pbc[0], self.pbc[1], self.pbc[2], self.pbc[3])
				self.pbcSET = True



	def ReadVASPData(self,*filename):

		if self.pbcSET == False:
			raise NameError ("Error: PBC must be defined first ")


		if self.BiasStep == 0:
			raise NameError ("Error: BiasStep must be defined first ")

		if self.StartingV == -1:
			raise NameError ("Error: StartingV must be defined first ")

		


		Density=[]




		for j in range(0,len(filename)):
			f = open(filename[j], "r")
			print "Reading in file: "+ filename[j]
			size=[0,0,0]

			NumberOfPoints=[0,0,0]

			#Number of points required to obtain given res
			Points=[0,0,0]

			NumberOfAtoms=0

			

			counter=[1,1,1]
		
			for linenumber, line in enumerate(f):
				#Find super cell size
				if linenumber == 2:
					size[0] = (float(line.split()[0])**2 + float(line.split()[1])**2 + float(line.split()[2])**2) ** (0.5)
				
				if linenumber == 3:
					size[1] = (float(line.split()[0])**2 + float(line.split()[1])**2 + float(line.split()[2])**2) ** (0.5)

				if linenumber == 4:
					size[2] = (float(line.split()[0])**2 + float(line.split()[1])**2 + float(line.split()[2])**2) ** (0.5)

				#Find number of atoms
				if linenumber == 6:
					for i in range(0, (len(line.split()))  ):
						NumberOfAtoms += float(line.split()[i])
					

				#find number of points
				if linenumber == NumberOfAtoms+9:

					NumberOfPoints[0]= float(line.split()[0])
					NumberOfPoints[1]= float(line.split()[1])
					NumberOfPoints[2]= float(line.split()[2])

				if linenumber > NumberOfAtoms+9:
					for i in range(0, (len(line.split()))  ):
						#Divide by volume 
						# 
						Density.append( float(line.split()[i])/ (size[0]*size[1]*size[2]) )
					
					if len(line.split()) < 10:
						break

			f.close()


			
		#Find step size
		dx = float(size[0]/NumberOfPoints[0])
		dy = float(size[1]/NumberOfPoints[1])
		dz = float(size[2]/NumberOfPoints[2])
		dv = float(self.BiasStep)
		#Find number of points
		nx = int(NumberOfPoints[0])
		ny = int(NumberOfPoints[1])
		nz = int(NumberOfPoints[2])
		nv = int(len(filename))

		#Set up Ctypes
		Circuit.cCore.i4Dlin_SetUpData.restype =  ctypes.POINTER(ctypes.POINTER(ctypes.c_double))
		Circuit.cCore.i4Dlin_SetUpData.argtypes = [ctypes.c_int 
												  ,ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, 
												   ctypes.c_double,  ctypes.c_double,  ctypes.c_double,  ctypes.c_double
												   ,  ctypes.c_double]
		#Pass some data to C
		self.data = Circuit.cCore.i4Dlin_SetUpData(self.cCoreID, nx , ny , nz, nv , dx, dy, dz , dv,  self.StartingV)

		#Move array from python to C
		for c in range(0,self.components):
			for index in range(0, len(Density)):

				self.data[c][index] = Density[index + c*index]

		#Clear array to free up memory
		del Density[0:len(Density)]






## \brief quad-linear interpolation circuit.
#
# \image html i4dlin.png "schema"
#
# This is the circuit that calculates the interpolation of the provided 4d force field.
# The force field must be in the following format, but plese note that the interpolation circuit is capable of taking any number of components in. 
#
# x y z v F1 F2 F3 
#
# The force field must also use a constant step size for each dimenson, although the force field can be in any order. The x y and z must also be the index
# of the point eg: 1 1 1 1 , 1 1 1 2 , 1 1 1 3 etc. When you configure the circuit later on you set the steps size to whatever you want it to be.
#
# - \b Initialisation \b parameters:.
# 	- \a Components = Number of components of force in the force field.
# 	- \a pushed True|False
# - \b Initialisation \b commands:
#	- Configure(steps=array, npoints=integer, pbc=True|False, ForceMultipler=float)
#		- \a steps = step size of the force field must be specfied in this format [x,y,z,v]
#		- \a npoints = number of points in each dimension must be specfied in this format [xn,yn,zn,vn]
#		- \a pbc = Perodic boundray conditions for each dimenson, must be specfied in this format [True|False,True|False,True|False,True|False]
#	-  ForceMultipler = A global multipler for all the force field values, use this to change the units of the force field into what ever units are desired.
#	-  ReadData(filename = string)
#		- \a Filename is the force field being interpolated.
# - \b Input \b channels:
#	 - \a x : this is x the coordiante to calculate the interpolation.
#	 - \a y : this is y the coordiante to calculate the interpolation.
#	 - \a z : this is z the coordiante to calculate the interpolation.
#	 - \a V : this is V the coordiante to calculate the interpolation.
# - \b Output \b channels:
# 	- \a Fn: The interpolated forces where n is the component for example F1 would be first first component.
#
# \b Example:
# \code
#	inter = machine.AddCircuit(type='i4Dlin',name='inter', components=1, pushed=True)
#	inter.Configure(steps=[0.805714285714286,0.805714285714286,0.1,0.1], npoints=[8,8,171,100])
#	inter.Configure(pbc=[True,True,False,False])
#	inter.ForceMultipler=1e10
#	inter.ReadData('4dData.dat')
# \endcode

class i4Dlin(Circuit):
    
    
	def __init__(self, machine, name, **keys):        
			
		super(self.__class__, self).__init__( machine, name )
		
		if 'components' in keys.keys():
			self.components = keys['components']
			print "components = " +str(self.components)
		else:
			raise NameError("No components entered ")
	

		Circuit.cCore.Add_i4Dlin.argtypes = [ctypes.c_int,ctypes.c_int]
		self.cCoreID = Circuit.cCore.Add_i4Dlin(machine.cCoreID, self.components)
		self.BiasStep=0
		self.StartingV=1
		self.pbcSET = False
		self.ForceMultiplier = 1
		self.AddInput("x")
		self.AddInput("y")
		self.AddInput("z")
		self.AddInput("V")


		for i in range(0,self.components):
			self.AddOutput("F"+str(i))

		self.SetInputs(**keys)

	def Configure(self, **keys):
				#check for pbc
		if 'pbc' in keys.keys():
			if len(keys['pbc']) != 4:
				raise ValueError("ERROR! the PBC requires 4 argments!")
			else:
				self.pbc = [0,0,0,0]
				for i in xrange(len(keys['pbc'])):
					if keys['pbc'][i] == True:
						self.pbc[i] = 1
					else:
						self.pbc[i] = 0
				
				Circuit.cCore.i4DLinPBC(self.cCoreID, self.pbc[0], self.pbc[1], self.pbc[2], self.pbc[3])
				self.pbcSET = True

		if 'points' in keys.keys():
			if len(keys['points']) != 4:
				raise ValueError("ERROR! the number of points requires 4 arguments! (nx,ny,nz,nv)")
			else:
				self.NPoints = [keys['points'][0],keys['points'][1],keys['points'][2],keys['points'][3]]


		if 'step' in keys.keys():
			if len(keys['step']) != 4:
				raise ValueError("ERROR! the step size requires 4 arguments! (nx,ny,nz,nv)")
			else:
				self.DX= keys['step'][0]
				self.DY= keys['step'][1]
				self.DZ= keys['step'][2]
				self.DV= keys['step'][3]






	def ReadData(self,*filename):

		if self.pbcSET == False:
			raise NameError ("Error: PBC must be defined first ")

		if self.StartingV == -1:
			raise NameError ("Error: StartingV must be defined first ")

		


		Density=[]




			
		#Find step size
		dx = self.DX
		dy = self.DY
		dz = self.DZ
		dv = self.DV
		#Find number of points
		nx = int(self.NPoints[0])
		ny = int(self.NPoints[1])
		nz = int(self.NPoints[2])
		nv = int(self.NPoints[3])

		#Set up Ctypes
		Circuit.cCore.i4Dlin_SetUpData.restype =  ctypes.POINTER(ctypes.POINTER(ctypes.c_double))
		Circuit.cCore.i4Dlin_SetUpData.argtypes = [ctypes.c_int 
												  ,ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, 
												   ctypes.c_double,  ctypes.c_double,  ctypes.c_double,  ctypes.c_double
												   ,  ctypes.c_double]
		#Pass some data to C
		self.data = Circuit.cCore.i4Dlin_SetUpData(self.cCoreID, nx , ny , nz, nv , dx, dy, dz , dv,  self.StartingV)



		f = open(filename, "r")
		for line in f:
			words = line.split()
			i = int(words[0])-1
			j = int(words[1])-1
			k = int(words[2])-1
			v = int(words[3])-1
			index = i + j*nx + k*nx*ny + v*nx*ny*nz
			for c in xrange(self.components): #convert the components to float
				words[c+4] = ctypes.c_double(float(words[c+4]) * self.ForceMultiplier)
				self.data[c][index] = words[c+4]
		
		f.close()

## \brief MechAfmToPyVafm circuit.
# 
# This circuit takes as an input a set of force files produced by the MechAFM then converts them to a PyVAFM compatible force field
# This requires a fodler to be in the same location as your input script that contains all the force field files from the MechAFM
#
# This circuit extracts the step size and number of points from the force files and stores them in the MaxInd and Step variable within the class
#
# If the file already exists in the folder then the conversion is skipped and only the step and number of points are extracted.
# To override this behaviour use the overide = True command
#
# - \b Initialisation \b parameters:.
# 	- \a foldername = Name of the folder that contains all the MechAFM force files.
#	- \a filename = Filename of the converted file
#   - \a overide = Overide the safey function to ensure we dont overwrite a file
# 	- \a pushed True|False
#
#
# \b Example:
# \code
#FFdata = machine.AddCircuit(type='MechAfmToPyVafm',name='MtoP',foldername = "Cl_tip" ) 
#inter = machine.AddCircuit(type='i3Dlin',name='inter', components=3, pushed=True) 
#inter.Configure(steps=FFdata.step, npoints=FFdata.MaxInd)
#inter.Configure(pbc=[True,True,False])
#inter.ReadData(FFdata.filename)
# \endcode

class MechAfmToPyVafm(Circuit):


	def __init__(self, machine, name, **keys):        
		
		super(self.__class__, self).__init__( machine, name )

		Folder=None
		self.filename = "ff.dat"
		overide=False
		self.step=None
		self.MaxInd=None

		if 'foldername' in keys.keys():
			Folder=keys['foldername']
		else:
			raise NameError ("Error: No folder specified")

		if 'filename' in keys.keys():
			self.filename=keys['filename']
		if "overide" in keys.keys():
			overide=keys['overide']


		#Check if ff.dat exists so we can easily debug
		import os.path
		FileExist = os.path.isfile(self.filename)
		if FileExist == True  and overide==False:
			print "####################################################################################"
			print "File already exists, skipping conversion, delete the file or change the filename"		
			print "####################################################################################"

		orignaldir = os.getcwd()+"/"
		os.chdir(orignaldir+Folder)

		#List of files
		files = glob.glob('*.dat')
		print "Found " + str(len(files)) + " files in folder " + Folder
		#open one file and check the x y size
		f = open(files[-1],'r')
		x=[]
		y=[]
		z=[]
		Realx=[]
		Realy=[]
		Realz=[]

		for line in f: 
			x.append( int ( line.split()[1] ) )
			y.append( int ( line.split()[2] ) )
			Realx.append( float ( line.split()[3] ) )
			Realy.append( float ( line.split()[4] ) )

		for Name in files:
			Realz.append( float(Name.split('-')[-1][:-4] ))

		self.MaxInd = [ max(x)+1,max(y)+1 , len(files)]
		self.step = [ round(sorted(set(Realx))[-1],4) - sorted(set(Realx))[-2] , round(sorted(set(Realy))[-1],4) - sorted(set(Realy))[-2] , round( sorted(Realz)[-1] - sorted(Realz)[-2],4) ]
		print "Number of Points = " + str(self.MaxInd)
		print "Step Size = " + str(self.step)

		offset = int( min(Realz)/self.step[2] )


		if FileExist == False or overide==True:

			print "Converting MechAFM Force file to PyVAFM file"
			Fx = [[[0 for k in xrange(self.MaxInd[2])] for j in xrange(self.MaxInd[1])] for i in xrange(self.MaxInd[0])]
			Fy = [[[0 for k in xrange(self.MaxInd[2])] for j in xrange(self.MaxInd[1])] for i in xrange(self.MaxInd[0])]
			Fz = [[[0 for k in xrange(self.MaxInd[2])] for j in xrange(self.MaxInd[1])] for i in xrange(self.MaxInd[0])]

			f.close()
			print "Reading in Files"
			counter = 0
			for FileName in files:
				if counter % 10 == 0:
					print  str ( round ( float ( counter) / float( self.MaxInd[2] ) * 100.0 , 2 ) ) + "% done"

				f = open(FileName,'r')
				for line in f:
					x= int ( line.split()[1] ) 
					y= int ( line.split()[2] ) 
					z= int ( line.split()[0] ) 
					Fx[x][y][z] = float ( line.split()[6] ) 
					Fy[x][y][z] = float ( line.split()[7] ) 
					Fz[x][y][z] = float ( line.split()[8] ) 
				counter +=1
			print "100% done"
	
		os.chdir(orignaldir)	

		if FileExist == False or overide==True:

			f = open(self.filename,'w')
			print "Writing force field file " + str(self.filename)
			for X in range(0,self.MaxInd[0]):
				for Y in range(0,self.MaxInd[1]):
					for Z in range(0,self.MaxInd[2]):
						f.write(str(X+1) + " " + str(Y+1) + " " + str(Z+1 + offset) + " " +  str(Fx[X][Y][self.MaxInd[2]-1 - Z]) + " " + str(Fy[X][Y][self.MaxInd[2]-1 - Z]) + " " + str(Fz[X][Y][self.MaxInd[2]-1 - Z]) + "\n" )
			f.close()
		self.MaxInd[2] += offset
