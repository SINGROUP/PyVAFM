from vafmbase import Circuit
import math
import ctypes
import numpy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import time
import math
import tools

class PlotAtoms(Circuit):
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )	

		if 'Filename' in keys.keys():
			self.Filename=  str(keys['Filename'])
		else:
			raise ValueError("Input Filename Required")

		NumberOfAtoms = 0
		f = open(self.Filename, "r")
		ATOMSx=[]
		ATOMSy=[]
		ATOMSz=[]
		mag = [0,0,0]
		size = [[0,0,0], [0,0,0], [0,0,0]]


		for linenumber, line in enumerate(f):
			
 			if linenumber == 2:
				mag[0] = (float(line.split()[0])**2 + float(line.split()[1])**2 + float(line.split()[2])**2) ** (0.5)
				size[0][0] = float(line.split()[0])
				size[0][1] = float(line.split()[1])
				size[0][2] = float(line.split()[2])


			if linenumber == 3:
				mag[1] = (float(line.split()[0])**2 + float(line.split()[1])**2 + float(line.split()[2])**2) ** (0.5)
				size[1][0] = float(line.split()[0])
				size[1][1] = float(line.split()[1])
				size[1][2] = float(line.split()[2])


			if linenumber == 4:
				mag[2] = (float(line.split()[0])**2 + float(line.split()[1])**2 + float(line.split()[2])**2) ** (0.5)
				size[2][0] = float(line.split()[0])
				size[2][1] = float(line.split()[1])
				size[2][2] = float(line.split()[2])




			#Find number of atoms
			if linenumber == 6:
				for i in range(0, (len(line.split()))  ):
					NumberOfAtoms += float(line.split()[i])

			if linenumber > 7:
				#ATOMS[linenumber-9][]
				ATOMSx.append( float(line.split()[0]) ) 
				ATOMSy.append( float (line.split()[1]))
				ATOMSz.append( float(line.split()[2]) )


			if linenumber > NumberOfAtoms+6:
				break

		#Find Coordinates

		ATOMS=[[0.0,0.0,0.0] for i in xrange(int (NumberOfAtoms) )]



		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		#ax.set_xlim3d(0, size[0])
		#ax.set_ylim3d(0, size[1])
		#ax.set_zlim3d(0, size[2])

		for i in range(0,int(NumberOfAtoms) ):
			#Shift me along the first vector
			ATOMS[i][0] = ATOMSx[i] * size[0][0]
			ATOMS[i][1] = ATOMSx[i] * size[0][1]
			ATOMS[i][2] = ATOMSx[i] * size[0][2]

			#Shift me along the 2nd vector
			
			ATOMS[i][0] += ATOMSy[i] * size[1][0]
			ATOMS[i][1] += ATOMSy[i] * size[1][1]
			ATOMS[i][2] += ATOMSy[i] * size[1][2]

			#Shift me along the 2nd vector
			
			ATOMS[i][0] += ATOMSz[i] * size[2][0]
			ATOMS[i][1] += ATOMSz[i] * size[2][1]
			ATOMS[i][2] += ATOMSz[i] * size[2][2]
			
			ax.scatter(ATOMS[i][0],ATOMS[i][1],ATOMS[i][2])



		plt.plot([0,size[0][0]], [0, size[0][1]],[0, size[0][2]], 'k-')
		plt.plot([0,size[1][0]], [0, size[1][1]],[0, size[1][2]], 'k-')
		plt.plot([0,size[2][0]], [0, size[2][1]],[0, size[2][2]], 'k-')


		# For x + y
		plt.plot([size[1][0],size[0][0]+size[1][0]], [size[1][1], size[0][1]+size[1][1]],[size[1][2], size[0][2]+size[1][2]], 'k-')

		#Fro x + z
		plt.plot([size[2][0],size[0][0]+size[2][0]], [size[2][1], size[0][1]+size[2][1]],[size[2][2], size[0][2]+size[2][2]], 'k-')

		#For x + z + y
		plt.plot([size[2][0]+size[1][0],size[0][0]+size[2][0]+size[1][0]], [size[2][1]+size[1][1], size[0][1]+size[2][1]+size[1][1]],[size[2][2]+size[1][2], size[0][2]+size[2][2]+size[1][2]], 'k-')



		#Complete the cell

		# For y + x
		plt.plot([size[0][0],size[1][0]+size[0][0]], [size[0][1], size[1][1]+size[0][1]],[size[0][2], size[1][2]+size[0][2]], 'k-')

		#For y + z
		plt.plot([size[2][0],size[1][0]+size[2][0]], [size[2][1], size[1][1]+size[2][1]],[size[2][2], size[1][2]+size[2][2]], 'k-')

		# For y +z + x
		plt.plot([size[2][0]+size[0][0],size[1][0]+size[2][0]+size[0][0]], [ size[2][1]+size[0][1], size[1][1]+size[2][1]+size[0][1]  ],[size[2][2]+size[0][2], size[1][2]+size[2][2]+size[0][2]], 'k-')


		# For z + x
		plt.plot([size[0][0],size[2][0]+size[0][0]], [size[0][1], size[2][1]+size[0][1]],[size[0][2], size[2][2]+size[0][2]], 'k-')

		#For z + y
		plt.plot([size[1][0],size[2][0]+size[1][0]], [size[1][1], size[2][1]+size[1][1]],[size[1][2], size[2][2]+size[1][2]], 'k-')

		# For z +y + x
		plt.plot([size[0][0]+size[1][0],size[1][0]+size[2][0]+size[0][0]], [ size[1][1]+size[0][1], size[1][1]+size[2][1]+size[0][1]  ],[size[1][2]+size[0][2], size[1][2]+size[2][2]+size[0][2]], 'k-')

		plt.show()
				

	

	def Initialize (self):
		pass


	def Update (self):
		pass		

class Dipole(Circuit):


	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		if 'PotentialFilename' in keys.keys():
			self.Filename=  str(keys['PotentialFilename'])
		else:
			raise ValueError("Input filename Required")


		if 'OutputFilename' in keys.keys():
			self.OFilename=  str(keys['OutputFilename'])
		else:
			raise ValueError("Output filename Required")


		f = open(self.Filename, "r")
		fo = open(self.OFilename, "w")
		print "Reading in file: "+ self.Filename


		size=[0,0,0]
		index = [0,0,0]
		NumberOfPoints=[0,0,0]

		Points=[0,0,0]

		NumberOfAtoms=0
		Vx =[0,0,0]
		Vy =[0,0,0]
		Vz =[0,0,0]

		linelen = 0
		check = False

		for linenumber, line in enumerate(f):
			if linenumber == 2:
				size[0] = (float(line.split()[0])**2 + float(line.split()[1])**2 + float(line.split()[2])**2) ** (0.5)
				
				Vx[0] = float(line.split()[0])
				Vx[1] = float(line.split()[1])
				Vx[2] = float(line.split()[2])

			if linenumber == 3:
				size[1] = (float(line.split()[0])**2 + float(line.split()[1])**2 + float(line.split()[2])**2) ** (0.5)

				Vy[0] = float(line.split()[0])
				Vy[1] = float(line.split()[1])
				Vy[2] = float(line.split()[2])

			if linenumber == 4:
				size[2] = (float(line.split()[0])**2 + float(line.split()[1])**2 + float(line.split()[2])**2) ** (0.5)


				Vz[0] = float(line.split()[0])
				Vz[1] = float(line.split()[1])
				Vz[2] = float(line.split()[2])
			
			#Find number of atoms
			if linenumber == 6:
				for i in range(0, (len(line.split()))  ):
					NumberOfAtoms += float(line.split()[i])


			#find number of points
			if linenumber == NumberOfAtoms+9:

				NumberOfPoints[0]= int(line.split()[0])
				NumberOfPoints[1]= int(line.split()[1])
				NumberOfPoints[2]= int(line.split()[2])



				V = [[[0 for k in xrange( int (NumberOfPoints[2]) ) ] for j in xrange( int (NumberOfPoints[1]) )] for i in xrange(int (NumberOfPoints[0]) )]
				#V = []				

			if linenumber > NumberOfAtoms+9:

				for i in range(0, (len(line.split()))  ):


					
					V[ index[0] ][ index[1] ] [ index[2] ] = float (line.split()[i])
					#V.append(float( line.split()[i] ) )
					#print index
					index[0] = index[0] +1

					if index [0] == NumberOfPoints[0]:
						index[0] = 0
						index[1] = index [1] +1

					if index [1] == NumberOfPoints[1]:
						index[1] = 0
						index[2] = index[2] +1	
				

				if len(line.split()) == 0:
					break

		print "File read in"
		#Find step size
		dx = float(size[0]/NumberOfPoints[0])
		dy = float(size[1]/NumberOfPoints[1])
		dz = float(size[2]/NumberOfPoints[2])
		
			


		print "Interpolating"

		stepx = 0.1
		stepy = 0.1
		stepz = 0.1

		Data = [[[0 for k in xrange( int (math.floor(size[2]/stepz)) ) ] for j in xrange( int (math.floor(size[1]/stepy)) )] for i in xrange(int (math.floor(size[0]/stepx)) )]


		counterz = 0
		countery = 0
		counterx = 0


		#interpolated point (in terms of magnitidue of the vector)
		x=0
		y=0
		z=0
		
		
		while x < size[0]-stepx:
			y=0
			while y < size[1]-stepy:
				z = 0
				while z < size[2]-stepz:
		

					indexpoint =[0,0,0]
					index =[0,0,0]


					#Find the voxel the point is 		
					index[0] = int(math.floor(x/dx)) 
					index[1] = int(math.floor(y/dy)) 
					index[2] = int(math.floor(z/dz)) 
					

					indexpoint[0] = x/dx
					indexpoint[1] = y/dy
					indexpoint[2] = z/dz

					#Find fractional indexs

					fracx = indexpoint[0]-index[0]
					fracy = indexpoint[1]-index[1]
					fracz = indexpoint[2]-index[2]
					#print fracx,fracy,fracz
					
					points = []
					values = []


					Data[counterx][countery][counterz] = (  V[index[0] ][ index[1] ][ index[2] ]*(1-fracx)*(1-fracy)*(1-fracz)  		#V000 * (1-x)*(1-y)*(1-z)

			       			 + V[index[0]+1 ][ index[1] ][ index[2] ]*(fracx)*(1-fracy)*(1-fracz)  		#V100 * (x)*(1-y)*(1-z) 

			       			 + V[index[0] ][ index[1]+1 ][ index[2] ]*(1-fracx)*(fracy)*(1-fracz)  		#V010 * (1-x)*(y)*(1-z) 

			       			 + V[index[0] ][ index[1] ][ index[2]+1 ]*(1-fracx)*(1-fracy)*(fracz)  		#V001 * (1-x)*(1-y)*(z)

			       			 + V[index[0]+1 ][ index[1] ][ index[2]+1 ]*(fracx)*(1-fracy)*(fracz)  		#V101 * (x)*(1-y)*(z)

			       			 + V[index[0] ][ index[1]+1 ][ index[2]+1 ]*(1-fracx)*(fracy)*(fracz) 		#V011 * (1-x)*(y)*(z)

			       			 + V[index[0]+1 ][ index[1]+1 ][ index[2] ]*(fracx)*(fracy)*(1-fracz)		#V110 * (x)*(y)*(1-z) 

			       			 + V[index[0]+1 ][ index[1]+1 ][ index[2]+1 ]*(fracx)*(fracy)*(fracz) )		#V111 * (x)*(y)*(z)

			 		z += stepz
			 		counterz += 1

			 	countery +=1
			 	counterz = 0
			 	y += stepy

			counterx+=1
			countery=0
			x += stepx
				
		Datax = len(Data)
		Datay = len(Data[0])
		Dataz = len(Data[0][0])

		#print Data[0][0][300]


		Force = [[[0 for k in xrange( int (Dataz) ) ] for j in xrange( int (Datay) )] for i in xrange(int (Datax) )]
		Forceb = [[[0 for k in xrange( int (Dataz) ) ] for j in xrange( int (Datay) )] for i in xrange(int (Datax) )]
		
		print "Calculating Derivatives"


		for x in range(0,Datax):
			for y in range(0,Datay):
				for z in range(0,Dataz-2):
					Force[x][y][z] = (Data[x][y][z+2] - Data[x][y][z]) / (stepz*2)


		for x in range(0,Datax):
			for y in range(0,Datay):
				for z in range(0,Dataz-4):
					Forceb[x][y][z] = (Force[x][y][z+2] - Force[x][y][z]) / (stepz*2)

		print "Writing to File"
		for x in range(0,Datax):
			for y in range(0,Datay):
				for z in range(0,Dataz-4):
					#print x,y,z
					fo.write(str(x+1)+" "+str(y+1)+" "+str(z+1)+" "+str(Forceb[x][y][z]) + "\n")		

		print size


	def Initialize (self):
		pass


	def Update (self):
		pass
	

