from vafmbase import Circuit
import math
import ctypes
import numpy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class PlotAtoms(Circuit):
    def __init__(self, machine, name, **keys):

        super(self.__class__, self).__init__(machine, name)

        if 'Filename' in list(keys.keys()):
            self.Filename = str(keys['Filename'])
        else:
            raise ValueError("Input Filename Required")

        NumberOfAtoms = 0
        f = open(self.Filename, "r")
        ATOMSx = []
        ATOMSy = []
        ATOMSz = []
        size = [0, 0, 0]

        for linenumber, line in enumerate(f):

            if linenumber == 2:
                size[0] = (float(line.split()[0])**2 + float(line.split()
                                                             [1])**2 + float(line.split()[2])**2) ** (0.5)

            if linenumber == 3:
                size[1] = (float(line.split()[0])**2 + float(line.split()
                                                             [1])**2 + float(line.split()[2])**2) ** (0.5)

            if linenumber == 4:
                size[2] = (float(line.split()[0])**2 + float(line.split()
                                                             [1])**2 + float(line.split()[2])**2) ** (0.5)

            # Find number of atoms
            if linenumber == 6:
                for i in range(0, (len(line.split()))):
                    NumberOfAtoms += float(line.split()[i])

            if linenumber > 7:
                # ATOMS[linenumber-9][]
                ATOMSx.append(float(line.split()[0]) * size[0])
                ATOMSy.append(float(line.split()[1]) * size[1])
                ATOMSz.append(float(line.split()[2]) * size[2])

            if linenumber > NumberOfAtoms+6:
                break

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim3d(0, size[0])
        ax.set_ylim3d(0, size[1])
        ax.set_zlim3d(0, size[2])

        ax.scatter(ATOMSx, ATOMSy, ATOMSz)
        plt.show()

    def Initialize(self):
        pass

    def Update(self):
        pass


class Dipole(Circuit):

    def __init__(self, machine, name, **keys):

        super(self.__class__, self).__init__(machine, name)

        if 'Dx' in list(keys.keys()):
            self.Dx = keys['Dx']
        else:
            raise ValueError("Dx Required")

        if 'Dy' in list(keys.keys()):
            self.Dy = keys['Dy']
        else:
            raise ValueError("Dy Required")

        if 'Dz' in list(keys.keys()):
            self.Dz = keys['Dz']
        else:
            raise ValueError("Dz Required")

        if 'PotentialFilename' in list(keys.keys()):
            self.Filename = str(keys['PotentialFilename'])
        else:
            raise ValueError("Input filename Required")

        if 'OutputFilename' in list(keys.keys()):
            self.OFilename = str(keys['OutputFilename'])
        else:
            raise ValueError("Output filename Required")

        if 'ZOffsetUpper' in list(keys.keys()):
            self.ZOffsetUpper = keys['ZOffsetUpper']
        else:
            self.ZOffsetUpper = 0

        if 'ZOffsetLower' in list(keys.keys()):
            self.ZOffsetLower = keys['ZOffsetLower']
        else:
            self.ZOffsetLower = 1

        if 'ConvertionFactor' in list(keys.keys()):
            self.ConvertionFactor = keys['ConvertionFactor']
        else:
            self.ConvertionFactor = 1

        if 'DerivativeStep' in list(keys.keys()):
            self.DerivativeStep = keys['DerivativeStep']
        else:
            self.DerivativeStep = int(1)

        if 'Step' in list(keys.keys()):
            self.step = keys['Step']
        else:
            self.step = int(1)

        if self.Filename == self.OFilename:
            raise NameError("Input and output file names must be different")

        f = open(self.Filename, "r")
        fo = open(self.OFilename, "w")
        print("Reading in file: " + self.Filename)
        size = [0, 0, 0]
        index = [1, 1, 1]
        NumberOfPoints = [0, 0, 0]

        # Number of points required to obtain given res
        Points = [0, 0, 0]

        NumberOfAtoms = 0

        for linenumber, line in enumerate(f):
            if linenumber == 2:
                size[0] = (float(line.split()[0])**2 + float(line.split()
                                                             [1])**2 + float(line.split()[2])**2) ** (0.5)

            if linenumber == 3:
                size[1] = (float(line.split()[0])**2 + float(line.split()
                                                             [1])**2 + float(line.split()[2])**2) ** (0.5)

            if linenumber == 4:
                size[2] = (float(line.split()[0])**2 + float(line.split()
                                                             [1])**2 + float(line.split()[2])**2) ** (0.5)

            # Find number of atoms
            if linenumber == 6:
                for i in range(0, (len(line.split()))):
                    NumberOfAtoms += float(line.split()[i])

            # find number of points
            if linenumber == NumberOfAtoms+9:

                NumberOfPoints[0] = float(line.split()[0])
                NumberOfPoints[1] = float(line.split()[1])
                NumberOfPoints[2] = float(line.split()[2])
                V = [[[0 for k in range(int(NumberOfPoints[2]+1))] for j in range(
                    int(NumberOfPoints[1]+1))] for i in range(int(NumberOfPoints[0]+1))]

            '''
			if linenumber > NumberOfAtoms+9:

				for i in range(0, (len(line.split()))  ):


					
					V[ index[0] ][ index[1] ] [ index[2] ] = float (line.split()[i])

					#print index
					index[0] = index[0] +1

					if index [0] == NumberOfPoints[0]+1:
						index[0] = 1
						index[1] = index [1] +1

					if index [1] == NumberOfPoints[1]+1:
						index[1] = 1
						index[2] = index[2] +1	

				if len(line.split()) == 0:
					break
				'''

        print("File Read in preforming derivatives ")

        # Find step size
        dx = float(size[0]/NumberOfPoints[0])
        dy = float(size[1]/NumberOfPoints[1])
        dz = float(size[2]/NumberOfPoints[2])

        # Find number of points
        nx = int(NumberOfPoints[0])
        ny = int(NumberOfPoints[1])
        nz = int(NumberOfPoints[2])

        step = self.step
        # From 1 to n
        rangex = list(range(1, nx+1, step))
        rangey = list(range(1, ny+1, step))

        # from offset to n-1-offset
        # eg: 0 to n-2
        rangez = list(range(self.ZOffsetLower, nz -
                            self.ZOffsetUpper+1-self.DerivativeStep, step))

        # Do the derviatives
        dzV = [[[0 for k in range(int(NumberOfPoints[2]+1))] for j in range(
            int(NumberOfPoints[1]+1))] for i in range(int(NumberOfPoints[0]+1))]

        '''
		#Find dz
		for z in rangez:
			for y in rangey:
				for x in rangex:
					#dzV = v[z+step] - V[z] / step
					dzV[x][y][z] = (V[x][y][z+self.DerivativeStep]-V[x][y][z])/ (dz*self.DerivativeStep)
		'''

        f.close()

        print("Force field calculated writing to filename: " + str(self.OFilename))

        index = [1, 1, 1]

        # Find dzdz, dydz and dxdz
        # make an array from 1 to n
        results = numpy.empty(shape=(nx+0, ny+0, nz+0, 3))

        '''
		for z in range(self.ZOffsetLower,nz-self.ZOffsetUpper+0-self.DerivativeStep,step):
		    for y in range(1,ny-self.DerivativeStep+0,step):
		        for x in range(1,nx-self.DerivativeStep+0,step):
					results[x][y][z][0] = self.ConvertionFactor * ( (dzV[x+self.DerivativeStep][y][z] - dzV[x][y][z] )/ (dx*self.DerivativeStep) )
					results[x][y][z][1] = self.ConvertionFactor * ( (dzV[x][y+self.DerivativeStep][z] - dzV[x][y][z] )/ (dy*self.DerivativeStep) )
					results[x][y][z][2] = self.ConvertionFactor * ( (dzV[x][y][z+self.DerivativeStep] - dzV[x][y][z] )/ (dz*self.DerivativeStep) )
					#print dzV[1][1][1] ,dzV[1][1][2] 
		'''

        counter = -1
        for z in range(self.ZOffsetLower, nz-self.ZOffsetUpper+0-self.DerivativeStep, step):
            for y in range(1, ny-self.DerivativeStep+0, step):
                for x in range(1, nx-self.DerivativeStep+0, step):
                    counter = counter + 1
                    if counter % 2 == 0:

                        fo.write(
                            str(index[0]) + " " + str(index[1]) + " " + str(index[2]) + " ")

                        '''
						if self.Dx > 0:
							fo.write(str(results[x,y,z,0]*self.Dx)+ "  ")
						if self.Dy > 0:
							fo.write(str(results[x,y,z,1]*self.Dy)+ "  ")
						if self.Dz > 0:
							fo.write(str(results[x,y,z,2]*self.Dz))
						'''
                        fo.write("\n")

                        index[0] = index[0] + 1

                        if index[0] >= NumberOfPoints[0]/2+0-self.DerivativeStep:
                            index[0] = 1
                            index[1] = index[1] + 1

                        if index[1] >= NumberOfPoints[1]/2+0-self.DerivativeStep:
                            index[1] = 1
                            index[2] = index[2] + 1

        fo.close()

        print(counter)
        foo = open(self.OFilename + ".info", "w")
        foo.write("Stepsze in x :" + " " + str(dx*self.DerivativeStep) + "\n")
        foo.write("Stepsze in y :" + " " + str(dy*self.DerivativeStep) + "\n")
        foo.write("Stepsze in z :" + " " + str(dz*self.DerivativeStep) + "\n")

        foo.write("Number Of points in x :" + " " + str(nx-2) + "\n")
        foo.write("Number Of points in y :" + " " + str(ny-2) + "\n")
        foo.write("Number Of points in z :" + " " + str(nz-2))

        foo.close()

    def Initialize(self):
        pass

    def Update(self):
        pass
