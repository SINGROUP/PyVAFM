#import GausSmear as GS
from vafmbase import Circuit
import numpy as np
import tools
import math


def gauss(real_dir2cart, grid_dim, real_grid_data, sigma):

    cent_point_grid = (np.floor(np.multiply(
        np.array([0.5, 0.5, 0.5]), grid_dim))).astype(int)

    dk = np.linalg.inv(real_dir2cart).T

    shift_filt_matrix = np.zeros(grid_dim)

    i = np.subtract(np.array(list(range(0, grid_dim[0]))), cent_point_grid[0])
    j = np.subtract(np.array(list(range(0, grid_dim[1]))), cent_point_grid[1])
    k = np.subtract(np.array(list(range(0, grid_dim[2]))), cent_point_grid[2])

    # NOTE STUPID ORDERING OF 3D MESHGRID OUTPUT !
    jj, ii, kk = np.meshgrid(j, i, k)

    xx = np.multiply(ii, dk[0, 0]) + np.multiply(jj,
                                                 dk[0, 1]) + np.multiply(kk, dk[0, 2])
    yy = np.multiply(ii, dk[1, 0]) + np.multiply(jj,
                                                 dk[1, 1]) + np.multiply(kk, dk[1, 2])
    zz = np.multiply(ii, dk[2, 0]) + np.multiply(jj,
                                                 dk[2, 1]) + np.multiply(kk, dk[2, 2])

    arg = np.multiply(np.multiply(xx, xx) + np.multiply(yy, yy) +
                      np.multiply(zz, zz), -2*np.pi**2*sigma**2)
    shift_filt_matrix = np.exp(arg)

    filt_matrix = np.fft.ifftshift(shift_filt_matrix)

    recip_grid_data = np.fft.fftn(real_grid_data)

    new_real_grid_data = np.fft.ifftn(
        np.multiply(recip_grid_data, filt_matrix))

    new_real_grid_data = np.multiply(
        np.sign(np.real(new_real_grid_data)), np.abs(new_real_grid_data))

    return new_real_grid_data


class GausSmear(Circuit):
    def __init__(self, machine, name, **keys):

        super(self.__class__, self).__init__(machine, name)

        if 'Filename' in list(keys.keys()):
            self.Filename = str(keys['Filename'])
        else:
            raise ValueError("Input Filename Required")

        if 'Sigma' in list(keys.keys()):
            self.Sigma = float(keys['Sigma'])
        else:
            raise ValueError("Sigma Required")

        if 'OutputFilename' in list(keys.keys()):
            self.OFilename = str(keys['OutputFilename'])
        else:
            raise ValueError("Output filename Required")

        check = False
        checka = False
        checkb = False
        checkc = False

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

        if 'ZCutOff' in list(keys.keys()):
            ZCutOff = keys['ZCutOff']
        else:
            ZCutOff = [0, 0]

        MakeSquare = False
        if 'MakeSquare' in list(keys.keys()):
            MakeSquare = keys['MakeSquare']
        else:
            MakeSquare = False

        fo = open(self.OFilename, "w")

        f = open(self.Filename, "r")

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

        linenumber = 0
        for line in f:

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
            linenumber = linenumber + 1

        if check == True:
            ForcefieldSize = [Vx[0], Vy[1], Vz[2]]

        if checka == True:
            LatticeVectora = [Vx[0], Vx[1], Vx[2]]

        if checkb == True:
            LatticeVectorb = [Vy[0], Vy[1], Vy[2]]

        if checkc == True:
            LatticeVectorc = [Vz[0], Vz[1], Vz[2]]

        print("File read in")
        f.close()
        # Find step size
        dx = float(size[0]/NumberOfPoints[0])
        dy = float(size[1]/NumberOfPoints[1])
        dz = float(size[2]/NumberOfPoints[2])

        Datax = len(V)
        Datay = len(V[0])
        Dataz = len(V[0][0])

        Lattice = [[Vx[0], Vx[1],  Vx[2]],
                   [Vy[0], Vy[1],  Vy[2]],
                   [Vz[0], Vz[1],  Vz[2]]]

        GridDim = [Datax, Datay, Dataz]

        Lattice = np.array(Lattice)
        GridDim = np.array(GridDim)
        V = np.array(V)

        OUT = gauss(Lattice, GridDim, V, self.Sigma)

        # Start making it square
        if check == True:
            ForcefieldSize = [Vx[0], Vy[1], Vz[2]]

        if checka == True:
            LatticeVectora = [Vx[0], Vx[1], Vx[2]]

        if checkb == True:
            LatticeVectorb = [Vy[0], Vy[1], Vy[2]]

        if checkc == True:
            LatticeVectorc = [Vz[0], Vz[1], Vz[2]]

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

                    ans = tools.interpolate(
                        OUT, [dx, dy, dz], posx, posy, posz)
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

        '''
		print "Writing to File"
		for x in range(0,Datax):
			for y in range(0,Datay):				
				for z in range(0,Dataz):
					#print x,y,z
					fo.write(str(x+1)+" "+str(y+1)+" "+str(z+1)+" "+str(OUT[x][y][z]) + "\n")
		'''
        fo.close()

    def Initialize(self):
        pass

    def Update(self):
        pass
