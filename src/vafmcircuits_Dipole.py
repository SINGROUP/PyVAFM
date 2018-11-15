from vafmbase import Circuit
import math
import ctypes
import numpy
#from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import time
import math
import tools

# \package vafmcircuits_Dipole
# This file contains the averager circuit classes.

# \brief PlotAtoms circuit.
#
# This circuit will plot atoms using MatPlotLib from a LOCPOT file.
# This Circuit requires MatPlotLib library to be installed.
#
# \b Initialisation \b parameters:
# 	- \a Filename = Input Filename | string
#
# \b Input \b channels:
# 	None
#
# \b Output \b channels:
# 	None
#
# \b Examples:
# \code{.py}
# machine.AddCircuit(type='PlotAtoms',name='plot',Filename='host.LOCPOT')
# \endcode
#


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
        mag = [0, 0, 0]
        size = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        for linenumber, line in enumerate(f):

            if linenumber == 2:
                mag[0] = (float(line.split()[0])**2 + float(line.split()
                                                            [1])**2 + float(line.split()[2])**2) ** (0.5)
                size[0][0] = float(line.split()[0])
                size[0][1] = float(line.split()[1])
                size[0][2] = float(line.split()[2])

            if linenumber == 3:
                mag[1] = (float(line.split()[0])**2 + float(line.split()
                                                            [1])**2 + float(line.split()[2])**2) ** (0.5)
                size[1][0] = float(line.split()[0])
                size[1][1] = float(line.split()[1])
                size[1][2] = float(line.split()[2])

            if linenumber == 4:
                mag[2] = (float(line.split()[0])**2 + float(line.split()
                                                            [1])**2 + float(line.split()[2])**2) ** (0.5)
                size[2][0] = float(line.split()[0])
                size[2][1] = float(line.split()[1])
                size[2][2] = float(line.split()[2])

            # Find number of atoms
            if linenumber == 6:
                for i in range(0, (len(line.split()))):
                    NumberOfAtoms += float(line.split()[i])

            if linenumber > 7:
                # ATOMS[linenumber-9][]
                ATOMSx.append(float(line.split()[0]))
                ATOMSy.append(float(line.split()[1]))
                ATOMSz.append(float(line.split()[2]))

            if linenumber > NumberOfAtoms+6:
                break

        # Find Coordinates

        ATOMS = [[0.0, 0.0, 0.0] for i in range(int(NumberOfAtoms))]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for i in range(0, int(NumberOfAtoms)):
            # Shift me along the first vector
            ATOMS[i][0] = ATOMSx[i] * size[0][0]
            ATOMS[i][1] = ATOMSx[i] * size[0][1]
            ATOMS[i][2] = ATOMSx[i] * size[0][2]

            # Shift me along the 2nd vector

            ATOMS[i][0] += ATOMSy[i] * size[1][0]
            ATOMS[i][1] += ATOMSy[i] * size[1][1]
            ATOMS[i][2] += ATOMSy[i] * size[1][2]

            # Shift me along the 3rd vector

            ATOMS[i][0] += ATOMSz[i] * size[2][0]
            ATOMS[i][1] += ATOMSz[i] * size[2][1]
            ATOMS[i][2] += ATOMSz[i] * size[2][2]

            ax.scatter(ATOMS[i][0], ATOMS[i][1], ATOMS[i][2])

        plt.plot([0, size[0][0]], [0, size[0][1]], [0, size[0][2]], 'k-')
        plt.plot([0, size[1][0]], [0, size[1][1]], [0, size[1][2]], 'k-')
        plt.plot([0, size[2][0]], [0, size[2][1]], [0, size[2][2]], 'k-')

        # For x + y
        plt.plot([size[1][0], size[0][0]+size[1][0]], [size[1][1], size[0]
                                                       [1]+size[1][1]], [size[1][2], size[0][2]+size[1][2]], 'k-')

        # Fro x + z
        plt.plot([size[2][0], size[0][0]+size[2][0]], [size[2][1], size[0]
                                                       [1]+size[2][1]], [size[2][2], size[0][2]+size[2][2]], 'k-')

        # For x + z + y
        plt.plot([size[2][0]+size[1][0], size[0][0]+size[2][0]+size[1][0]], [size[2][1]+size[1][1], size[0]
                                                                             [1]+size[2][1]+size[1][1]], [size[2][2]+size[1][2], size[0][2]+size[2][2]+size[1][2]], 'k-')

        # Complete the cell

        # For y + x
        plt.plot([size[0][0], size[1][0]+size[0][0]], [size[0][1], size[1]
                                                       [1]+size[0][1]], [size[0][2], size[1][2]+size[0][2]], 'k-')

        # For y + z
        plt.plot([size[2][0], size[1][0]+size[2][0]], [size[2][1], size[1]
                                                       [1]+size[2][1]], [size[2][2], size[1][2]+size[2][2]], 'k-')

        # For y +z + x
        plt.plot([size[2][0]+size[0][0], size[1][0]+size[2][0]+size[0][0]], [size[2][1]+size[0][1], size[1]
                                                                             [1]+size[2][1]+size[0][1]], [size[2][2]+size[0][2], size[1][2]+size[2][2]+size[0][2]], 'k-')

        # For z + x
        plt.plot([size[0][0], size[2][0]+size[0][0]], [size[0][1], size[2]
                                                       [1]+size[0][1]], [size[0][2], size[2][2]+size[0][2]], 'k-')

        # For z + y
        plt.plot([size[1][0], size[2][0]+size[1][0]], [size[1][1], size[2]
                                                       [1]+size[1][1]], [size[1][2], size[2][2]+size[1][2]], 'k-')

        # For z +y + x
        plt.plot([size[0][0]+size[1][0], size[1][0]+size[2][0]+size[0][0]], [size[1][1]+size[0][1], size[1]
                                                                             [1]+size[2][1]+size[0][1]], [size[1][2]+size[0][2], size[1][2]+size[2][2]+size[0][2]], 'k-')

        plt.show()

    def Initialize(self):
        pass

    def Update(self):
        pass


# \brief ExtractPotential circuit.
#
# This circuit will extract the potential from a cubic LOCPOT file, as well as outputting to the terminal information regarding the locpot eg: Stepsize etc.
#
# \b Initialisation \b parameters:
# 	- \a PotentialFilename = LOCPOT Filename | string
# 	- \a OutputFilename = Output Filename | string
#	- \a ZCutOff = [LowerIndex | int ,UpperIndex | int] This is the upper and lower z index cut offs allowings users to cut off top or bottom of locpot files
#
# \b Input \b channels:
# 	None
#
# \b Output \b channels:
# 	None
#
# \b Examples:
# \code{.py}
# machine.AddCircuit(type='ExtractPotential',name='host.LOCPOT', OutputFilename="File.dat",PotentialFilename=InputFilename,ZCutOff=[200,20])
# \endcode
#

# This will simple extract potential from a LOCPOT
class ExtractPotential(Circuit):

    def __init__(self, machine, name, **keys):

        super(self.__class__, self).__init__(machine, name)

        if 'PotentialFilename' in list(keys.keys()):
            self.Filename = str(keys['PotentialFilename'])
        else:
            raise ValueError("Input filename Required")

        if 'OutputFilename' in list(keys.keys()):
            self.OFilename = str(keys['OutputFilename'])
        else:
            raise ValueError("Output filename Required")

        check = False

        if 'ZCutOff' in list(keys.keys()):
            ZCutOff = keys['ZCutOff']
        else:
            ZCutOff = [0, 0]
            check = True

        f = open(self.Filename, "r")
        fo = open(self.OFilename, "w")
        print("Reading in file: " + self.Filename)

        size = [0, 0, 0]
        index = [0, 0, 0]
        NumberOfPoints = [0, 0, 0]

        Points = [0, 0, 0]

        NumberOfAtoms = 0
        Vx = [0, 0, 0]
        Vy = [0, 0, 0]
        Vz = [0, 0, 0]

        linelen = 0
        check = False

        for linenumber, line in enumerate(f):
            if linenumber == 2:
                size[0] = (float(line.split()[0])**2 + float(line.split()
                                                             [1])**2 + float(line.split()[2])**2) ** (0.5)

                Vx[0] = float(line.split()[0])
                Vx[1] = float(line.split()[1])
                Vx[2] = float(line.split()[2])

            if linenumber == 3:
                size[1] = (float(line.split()[0])**2 + float(line.split()
                                                             [1])**2 + float(line.split()[2])**2) ** (0.5)

                Vy[0] = float(line.split()[0])
                Vy[1] = float(line.split()[1])
                Vy[2] = float(line.split()[2])

            if linenumber == 4:
                size[2] = (float(line.split()[0])**2 + float(line.split()
                                                             [1])**2 + float(line.split()[2])**2) ** (0.5)

                Vz[0] = float(line.split()[0])
                Vz[1] = float(line.split()[1])
                Vz[2] = float(line.split()[2])

            # Find number of atoms
            if linenumber == 6:
                for i in range(0, (len(line.split()))):
                    NumberOfAtoms += float(line.split()[i])

            # find number of points
            if linenumber == NumberOfAtoms+9:

                NumberOfPoints[0] = int(line.split()[0])
                NumberOfPoints[1] = int(line.split()[1])
                NumberOfPoints[2] = int(line.split()[2])

                V = [[[0 for k in range(int(NumberOfPoints[2]))] for j in range(
                    int(NumberOfPoints[1]))] for i in range(int(NumberOfPoints[0]))]

            if linenumber > NumberOfAtoms+9:

                for i in range(0, (len(line.split()))):

                    V[index[0]][index[1]][index[2]] = float(line.split()[i])

                    index[0] = index[0] + 1

                    if index[0] == NumberOfPoints[0]:
                        index[0] = 0
                        index[1] = index[1] + 1

                    if index[1] == NumberOfPoints[1]:
                        index[1] = 0
                        index[2] = index[2] + 1

                if len(line.split()) == 0:
                    break

        print("File read in")
        # Find step size
        dx = float(size[0]/NumberOfPoints[0])
        dy = float(size[1]/NumberOfPoints[1])
        dz = float(size[2]/NumberOfPoints[2])

        Datax = len(V)
        Datay = len(V[0])
        Dataz = len(V[0][0])

        if check == True:
            ZCutOff[1] == Dataz

        print("Writing to File")
        for x in range(0, Datax):
            for y in range(0, Datay):
                for z in range(0, ZCutOff[1]):
                    # print x,y,z
                    fo.write(str(x+1)+" "+str(y+1)+" "+str(z+1 +
                                                           ZCutOff[0])+" "+str(V[x][y][z + ZCutOff[0]]) + "\n")

        print("####################################")
        print("Potential Field Information ")
        print(" ")
        print("Step size in x = " + str(dx))
        print("Step size in y = " + str(dy))
        print("Step size in z = " + str(dz))
        print(" ")
        print("Number of points in x is = " + str(NumberOfPoints[0]))
        print("Number of points in y is = " + str(NumberOfPoints[1]))
        print("Number of points in z is = " + str(ZCutOff[1]+ZCutOff[0]))
        print(" ")
        print("Lattice x vector is " + str(Vx) +
              " and the magnitude is " + str(size[0]))
        print("Lattice y vector is " + str(Vy) +
              " and the magnitude is " + str(size[1]))
        print("Lattice z vector is " + str(Vz) +
              " and the magnitude is " + str(size[2]))
        print(" ")
        print("####################################")

    def Initialize(self):
        pass

    def Update(self):
        pass


# \brief LOCPOTShaping circuit.
#
# This circuit will extract the potential from a LOCPOT file for both ortharombic and non orthorombic files. After extracting the potential
# the circuit will reshape the data into a cubic format so it can be read by the PyVAFM.
#
# \b Initialisation \b parameters:
# 	- \a PotentialFilename = LOCPOT Filename | string
# 	- \a OutputFilename = Output Filename | string
#	- \a ZCutOff = [LowerIndex | int ,UpperIndex | int] This is the upper and lower z index cut offs allowings users to cut off top or bottom of locpot files
#	- \a ForcefieldSize = [x | float ,y | float,z | float] This is the total size of the force field, By default this is set to the size of the appropriate component of the lattice vectors.
#	- \a ForcefieldStepSize = [x | float ,y | float,z | float] This is the step size of the force field,

#
# \b Input \b channels:
# 	None
#
# \b Output \b channels:
# 	None
#
# \b Examples:
# \code{.py}
# machine.AddCircuit(type='LOCPOTShaping',name='LOCPOTShaping', OutputFilename="Ceria.dat",PotentialFilename="host.LOCPOT",ForcefieldSize=[15.562592,13.4776,25.413607]
#					,ForcefieldStepSize=[0.072049037037,0.0748755555556,0.075635735119])
# \endcode
#


class LOCPOTShaping(Circuit):

    def __init__(self, machine, name, **keys):

        super(self.__class__, self).__init__(machine, name)

        if 'PotentialFilename' in list(keys.keys()):
            self.Filename = str(keys['PotentialFilename'])
        else:
            raise ValueError("Input filename Required")

        if 'OutputFilename' in list(keys.keys()):
            self.OFilename = str(keys['OutputFilename'])
        else:
            raise ValueError("Output filename Required")

        check = False
        checka = False
        checkb = False
        checkc = False

        if 'ZCutOff' in list(keys.keys()):
            ZCutOff = keys['ZCutOff']
        else:
            ZCutOff = [0, 0]

        if 'ForcefieldSize' in list(keys.keys()):
            ForcefieldSize = keys['ForcefieldSize']
        else:
            check = True
            ForcefieldSize = [15.562592, 13.4776, 25.413607]

        if 'ForcefieldStepSize' in list(keys.keys()):
            STEPSIZE = keys['ForcefieldStepSize']
        else:
            raise ValueError("ERROR: No Force field step size specified")

        stepx = STEPSIZE[0]
        stepy = STEPSIZE[1]
        stepz = STEPSIZE[2]

        if 'LatticeVectora' in list(keys.keys()):
            LatticeVectora = keys['LatticeVectora']
        else:
            checka = True

        if 'LatticeVectorb' in list(keys.keys()):
            LatticeVectorb = keys['LatticeVectorb']
        else:
            checkb = True

        if 'LatticeVectorc' in list(keys.keys()):
            LatticeVectorc = keys['LatticeVectorc']
        else:
            checkc = True

        f = open(self.Filename, "r")
        fo = open(self.OFilename, "w")
        print("Reading in file: " + self.Filename)

        size = [0, 0, 0]
        index = [0, 0, 0]
        NumberOfPoints = [0, 0, 0]

        Points = [0, 0, 0]

        NumberOfAtoms = 0
        Vx = [0, 0, 0]
        Vy = [0, 0, 0]
        Vz = [0, 0, 0]

        linelen = 0
        check = False

        for linenumber, line in enumerate(f):
            if linenumber == 2:
                size[0] = (float(line.split()[0])**2 + float(line.split()
                                                             [1])**2 + float(line.split()[2])**2) ** (0.5)

                Vx[0] = float(line.split()[0])
                Vx[1] = float(line.split()[1])
                Vx[2] = float(line.split()[2])

            if linenumber == 3:
                size[1] = (float(line.split()[0])**2 + float(line.split()
                                                             [1])**2 + float(line.split()[2])**2) ** (0.5)

                Vy[0] = float(line.split()[0])
                Vy[1] = float(line.split()[1])
                Vy[2] = float(line.split()[2])

            if linenumber == 4:
                size[2] = (float(line.split()[0])**2 + float(line.split()
                                                             [1])**2 + float(line.split()[2])**2) ** (0.5)

                Vz[0] = float(line.split()[0])
                Vz[1] = float(line.split()[1])
                Vz[2] = float(line.split()[2])

            # Find number of atoms
            if linenumber == 6:
                for i in range(0, (len(line.split()))):
                    NumberOfAtoms += float(line.split()[i])

            # find number of points
            if linenumber == NumberOfAtoms+9:

                NumberOfPoints[0] = int(line.split()[0])
                NumberOfPoints[1] = int(line.split()[1])
                NumberOfPoints[2] = int(line.split()[2])

                V = [[[0 for k in range(int(NumberOfPoints[2]))] for j in range(
                    int(NumberOfPoints[1]))] for i in range(int(NumberOfPoints[0]))]

            if linenumber > NumberOfAtoms+9:

                for i in range(0, (len(line.split()))):

                    V[index[0]][index[1]][index[2]] = float(line.split()[i])
                    index[0] = index[0] + 1

                    if index[0] == NumberOfPoints[0]:
                        index[0] = 0
                        index[1] = index[1] + 1

                    if index[1] == NumberOfPoints[1]:
                        index[1] = 0
                        index[2] = index[2] + 1

                if len(line.split()) == 0:
                    break

        if check == True:
            ForcefieldSize = [Vx[0], Vy[1], Vz[2]]

        if checka == True:
            LatticeVectora = [Vx[0], Vx[1], Vx[2]]

        if checkb == True:
            LatticeVectorb = [Vy[0], Vy[1], Vy[2]]

        if checkc == True:
            LatticeVectorc = [Vz[0], Vz[1], Vz[2]]

        print("File read in")
        # Find step size
        dx = float(size[0]/NumberOfPoints[0])
        dy = float(size[1]/NumberOfPoints[1])
        dz = float(size[2]/NumberOfPoints[2])

        Datax = len(V)
        Datay = len(V[0])
        Dataz = len(V[0][0])

        Force = [[[0 for k in range(int(Dataz))] for j in range(
            int(Datay))] for i in range(int(Datax))]
        Forceb = [[[0 for k in range(int(Dataz))] for j in range(
            int(Datay))] for i in range(int(Datax))]

        # For coord transform find:

        ax = LatticeVectora[0]
        ay = LatticeVectora[1]
        az = LatticeVectora[2]

        bx = LatticeVectorb[0]
        by = LatticeVectorb[1]
        bz = LatticeVectorb[2]

        cx = LatticeVectorc[0]
        cy = LatticeVectorc[1]
        cz = LatticeVectorc[2]

        maga = math.sqrt(LatticeVectora[0]*LatticeVectora[0] + LatticeVectora[1]
                         * LatticeVectora[1] + LatticeVectora[2]*LatticeVectora[2])
        magb = math.sqrt(LatticeVectorb[0]*LatticeVectorb[0] + LatticeVectorb[1]
                         * LatticeVectorb[1] + LatticeVectorb[2]*LatticeVectorb[2])
        magc = math.sqrt(LatticeVectorc[0]*LatticeVectorc[0] + LatticeVectorc[1]
                         * LatticeVectorc[1] + LatticeVectorc[2]*LatticeVectorc[2])

        print("Interpolating")

        x = 0
        y = 0
        z = 0

        counter = [0, 0, 0]

        sizex = math.ceil(ForcefieldSize[0] / stepx)
        sizey = math.ceil(ForcefieldSize[1] / stepy)
        sizez = math.ceil(ForcefieldSize[2] / stepz)

        U = [[[0 for k in range(int(sizez))] for j in range(
            int(sizey))] for i in range(int(sizex))]

        xarray = []
        yarray = []
        zarray = []

        # Build the 3d interpolated square grid
        while x <= ForcefieldSize[0]:
            while y <= ForcefieldSize[1]:
                while z <= ForcefieldSize[2]:

                    # Find the transformed coordiante
                    posx = maga*(bz*cy*x - by*cz*x - bz*cx*y + bx*cz*y + by*cx*z - bx*cy*z) / (
                        az*by*cx - ay*bz*cx - az*bx*cy + ax*bz*cy + ay*bx*cz - ax*by*cz)
                    posy = magb*(az*cy*x - ay*cz*x - az*cx*y + ax*cz*y + ay*cx*z - ax*cy*z) / \
                        (-(az*by*cx) + ay*bz*cx + az*bx *
                         cy - ax*bz*cy - ay*bx*cz + ax*by*cz)
                    posz = magc*(az*by*x - ay*bz*x - az*bx*y + ax*bz*y + ay*bx*z - ax*by*z) / (
                        az*by*cx - ay*bz*cx - az*bx*cy + ax*bz*cy + ay*bx*cz - ax*by*cz)

                    ans = tools.interpolate(V, [dx, dy, dz], posx, posy, posz)
                    U[counter[0]][counter[1]][counter[2]] = ans

                    z += stepz
                    counter[2] += 1

                counter[1] += 1
                counter[2] = 0
                z = 0
                y += stepy

            counter[0] += 1
            counter[1] = 0
            counter[2] = 0
            y = 0
            z = 0
            x += stepx

        # Output the Potential
        print("Writing to File")
        for x in range(0, int(sizex)):
            for y in range(0, int(sizey)):
                for z in range(0+ZCutOff[0], int(sizez-ZCutOff[1])):
                    fo.write(str(x+1)+" "+str(y+1)+" "+str(z+1) +
                             " " + str(U[x][y][z]) + "\n")

        fo.close()

    def Initialize(self):
        pass

    def Update(self):
        pass


# \brief Dipole circuit.
#
# This circuit will apply the dipole aproximation as devloped by David Gao (<http://pubs.acs.org/doi/abs/10.1021/nn501785q>).
# Warning: Be careful when applying this aproximation to noisy signals as the second derivatives may yeild an incorrect result.
#
# \b Initialisation \b parameters:
# 	- \a InputFile = Input potential file must be in the same format as used in i3dlin.
#	- \a OutputFile = Output force field already formated in such a way that the PyVAFM can use it.
#	- \a StepSize = Step size of the inputted potential field..
#	- \a Dz = Magnitude of the dipole vector in the z direction.

#
# \b Input \b channels:
# 	- None
#
# \b Output \b channels:
# 	- None
#
# \b Examples:
# \code{.py}
#machine.AddCircuit(type='Dipole',name='Dipole',InputFile="Ceria.dat", OutputFile="FF.dat", stepsize= [0.072049037037,0.0748755555556,0.075635735119])
# \endcode
#


class Dipole(Circuit):

    def __init__(self, machine, name, **keys):

        super(self.__class__, self).__init__(machine, name)

        if 'InputFile' in list(keys.keys()):
            self.Filename = str(keys['InputFile'])
        else:
            raise ValueError("Input filename Required")

        if 'OutputFile' in list(keys.keys()):
            self.OFilename = str(keys['OutputFile'])
        else:
            raise ValueError("Output filename Required")

        if 'stepsize' in list(keys.keys()):
            Step = keys['stepsize']
        else:
            raise ValueError("step size Required")

        if 'Dz' in list(keys.keys()):
            Dz = keys['Dz']
        else:
            Dz = 1

        f = open(self.Filename, "r")
        fo = open(self.OFilename, "w")
        print("Reading in file: " + self.Filename)

        for line in f:
            pass
        last = line

        if last == "\n":
            raise ValueError(
                "ERROR: Blank line at end of input file, remove it from input file")

        I = int(last.split()[0])
        J = int(last.split()[1])
        K = int(last.split()[2])

        U = [[[0 for k in range(int(K))] for j in range(int(J))]
             for i in range(int(I))]
        Force = [[[0 for k in range(int(K))]
                  for j in range(int(J))] for i in range(int(I))]

        f = open(self.Filename, "r")
        for line in f:

            U[int(line.split()[0])-1][int(line.split()[1]) -
                                      1][int(line.split()[2])-1] = float(line.split()[3])

        for x in range(0, I):
            for y in range(0, J):
                for z in range(1, K-2):
                    Force[x][y][z] = (U[x][y][z+2] - 2*U[x][y]
                                      [z] + U[x][y][z-2]) / (Step[2]*Step[2]) * Dz
                    #Force[x][y][z] = (-U[x][y][z+2] + 16*U[x][y][z+1] - 30*U[x][y][z] + 16*U[x][y][z-1] - U[x][y][z-2] )/(12*Step[2]*Step[2]) * Dz

        for x in range(0, I):
            for y in range(0, J):
                for z in range(1, K-2):
                    fo.write(str(x+1)+" "+str(y+1)+" "+str(z) +
                             " "+str(Force[x][y][z]) + "\n")

        fo.close()

    def Initialize(self):
        pass

    def Update(self):
        pass
