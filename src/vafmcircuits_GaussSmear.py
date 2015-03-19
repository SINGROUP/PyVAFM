import GausSmear as GS
from vafmbase import Circuit
import numpy as np


class GausSmear(Circuit):
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )	

		if 'Filename' in keys.keys():
			self.Filename=  str(keys['Filename'])
		else:
			raise ValueError("Input Filename Required")

		if 'Sigma' in keys.keys():
			self.Sigma=  float(keys['Sigma'])
		else:
			raise ValueError("Sigma Required")


		if 'OutputFilename' in keys.keys():
			self.OFilename=  str(keys['OutputFilename'])
		else:
			raise ValueError("Output filename Required")


		fo = open(self.OFilename, "w")

		f = open(self.Filename, "r")


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


		linenumber=0
		for line in f:
			
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
	
			
			if linenumber > NumberOfAtoms+9:

				for i in range(0, (len(line.split()))  ):


					V[ index[0] ][ index[1] ] [ index[2] ] = float (line.split()[i])
				
					index[0] = index[0] +1

					if index [0] == NumberOfPoints[0]:
						index[0] = 0
						index[1] = index [1] +1

					if index [1] == NumberOfPoints[1]:
						index[1] = 0
						index[2] = index[2] +1	
				

				if len(line.split()) == 0:
					break
			linenumber = linenumber + 1




		print "File read in"
		f.close()
		#Find step size
		dx = float(size[0]/NumberOfPoints[0])
		dy = float(size[1]/NumberOfPoints[1])
		dz = float(size[2]/NumberOfPoints[2])

		Datax = len(V)
		Datay = len(V[0])
		Dataz = len(V[0][0])

		Lattice = [ [Vx[0] ,Vx[1] ,  Vx[2]],
					[Vy[0] ,Vy[1] ,  Vy[2] ],
					[Vz[0] ,Vz[1] ,  Vz[2]] ]

		GridDim = [ Datax , Datay , Dataz ]

		Lattice=np.array(Lattice)
		GridDim=np.array(GridDim)
		V=np.array(V)


		OUT = GS.gauss(Lattice,GridDim,V,self.Sigma)



		print "Writing to File"
		for x in range(0,Datax):
			for y in range(0,Datay):				
				for z in range(0,Dataz):
					#print x,y,z
					fo.write(str(x+1)+" "+str(y+1)+" "+str(z+1)+" "+str(OUT[x][y][z]) + "\n")

	def Initialize (self):
		pass


	def Update (self):
		pass