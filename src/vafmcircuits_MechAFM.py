from vafmbase import Circuit
from vafmbase import ChannelType
from vafmbase import Channel
from ctypes import c_int
from subprocess import call
import math
import numpy

import numpy
import matplotlib
import os
import sys
import gzip
import glob
from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

# Stil waiting for peter to write a manual for this.


class MechAFM(Circuit):

    def __init__(self, machine, name, **keys):

        super(self.__class__, self).__init__(machine, name)

        if 'xyzfile' in list(keys.keys()):
            self.xyzfilename = str(keys['xyzfile'])
        else:
            raise NameError("Missing xyz file name!")

        if 'paramfile' in list(keys.keys()):
            self.paramfile = str(keys['paramfile'])
        else:
            raise NameError("Missing parameter file name!")

        if 'TipAtom' in list(keys.keys()):
            self.TipAtom = str(keys['TipAtom'])
        else:
            raise NameError("Missing TipAtom!")

        if 'DummyAtom' in list(keys.keys()):
            self.DummyAtom = str(keys['DummyAtom'])
        else:
            raise NameError("Missing dummyatom!")

        if 'PlaneAtom' in list(keys.keys()):
            self.PlaneAtom = str(keys['PlaneAtom'])
        else:
            raise NameError("Missing planeatom!")

        if 'MinTerm' in list(keys.keys()):
            self.MinTerm = str(keys['MinTerm'])
        else:
            raise NameError("Missing minimsation term!")

        if 'etol' in list(keys.keys()):
            self.etol = str(keys['etol'])
        else:
            raise NameError("Missing Energy Tolerance!")

        if 'ftol' in list(keys.keys()):
            self.ftol = str(keys['ftol'])
        else:
            raise NameError("Missing Force Tolerance!")

        if 'cfac' in list(keys.keys()):
            self.cfac = str(keys['cfac'])
        else:
            raise NameError("Missing cfac(Find out what this means again)")

        if 'cfac' in list(keys.keys()):
            self.cfac = str(keys['cfac'])
        else:
            raise NameError("Missing cfac(Find out what this means again)")

        if 'coulomb' in list(keys.keys()):
            self.coulomb = str(keys['coulomb'])
        else:
            raise NameError("Missing coulomb option")

        if 'zhigh' in list(keys.keys()):
            self.zhigh = str(keys['zhigh'])
        else:
            raise NameError("Missing zhigh")

        if 'zlow' in list(keys.keys()):
            self.zlow = str(keys['zlow'])
        else:
            raise NameError("Missing zlow")

        if 'dx' in list(keys.keys()):
            self.dx = str(keys['dx'])
        else:
            raise NameError("Missing dx")

        if 'dy' in list(keys.keys()):
            self.dy = str(keys['dy'])
        else:
            raise NameError("Missing dy")

        if 'dz' in list(keys.keys()):
            self.dz = str(keys['dz'])
        else:
            raise NameError("Missing dz")

        if 'bufsize' in list(keys.keys()):
            self.bufsize = str(keys['bufsize'])
        else:
            raise NameError("Missing buffer size")

        if 'InputFileName' in list(keys.keys()):
            self.InputFileName = str(keys['InputFileName'])
        else:
            raise NameError("Missing Input File Name")

        if 'MaxSteps' in list(keys.keys()):
            self.maxsteps = str(keys['MaxSteps'])
        else:
            raise NameError("Missing MaxSteps")

        if 'MPICommand' in list(keys.keys()):
            self.MPICommand = str(keys['MPICommand'])
        else:
            raise NameError("Missing MPICommand")

        fo = open(self.InputFileName, "w")

        fo.write("xyzfile      "+str(self.xyzfilename)+"\n")
        fo.write("paramfile    "+str(self.paramfile)+"\n")
        fo.write("tipatom      "+str(self.TipAtom)+"\n")
        fo.write("dummyatom    "+str(self.DummyAtom)+"\n")
        fo.write("planeatom    "+str(self.PlaneAtom)+"\n")
        fo.write("\n")
        fo.write("minterm      "+str(self.MinTerm)+"\n")
        fo.write("etol         "+str(self.etol)+"\n")
        fo.write("ftol         "+str(self.ftol)+"\n")
        fo.write("cfac         "+str(self.cfac)+"\n")
        fo.write("maxsteps     "+str(self.maxsteps)+"\n")
        fo.write("\n")
        fo.write("coulomb	     "+str(self.coulomb)+"\n")
        fo.write("\n")
        fo.write("zhigh	     "+str(self.zhigh)+"\n")
        fo.write("zlow         "+str(self.zlow)+"\n")
        fo.write("dx       "+str(self.dx)+"\n")
        fo.write("dy       "+str(self.dy)+"\n")
        fo.write("dz       "+str(self.dz)+"\n")
        fo.write("\n")
        fo.write("bufsize	     "+str(self.bufsize)+"\n")

        # ToDo check MPI is installed
        fo.close()
        os.system(str(self.MPICommand) +
                  " ./bin/mechafm-mpi "+str(self.InputFileName))

    def Initialize(self):

        pass

    def Update(self):
        pass


class SimpleAFM(Circuit):
    # Uniquify a list
    def uniquify(seq, idfun=None):
        if idfun is None:
            def idfun(x): return x
        seen = {}
        result = []
        for item in seq:
            marker = idfun(item)
            if marker in seen:
                continue
            seen[marker] = 1
            result.append(item)
        return result

    def __init__(self, machine, name, **keys):

        super(self.__class__, self).__init__(machine, name)

        if 'xyzfile' in list(keys.keys()):
            self.xyzfile = str(keys['xyzfile'])
        else:
            raise NameError("Missing xyz file name!")

        if 'frcfiles' in list(keys.keys()):
            self.frcfiles = str(keys['frcfiles'])
        else:
            raise NameError("Missing frcfiles !")

        if 'inpfile' in list(keys.keys()):
            self.inpfile = str(keys['inpfile'])
        else:
            raise NameError("Missing inpfile!")

        # Talk to me
        print('Setting some initial things')

        # Some basic settings
        xyzfile = self.xyzfile
        frcfiles = self.frcfiles
        inpfile = self.inpfile

        # Directory name
        f = open(inpfile, 'r')
        d = f.readlines()
        f.close()
        for line in d:
            if 'dx' in line:
                resx = float(line.split()[1])
            if 'dy' in line:
                resy = float(line.split()[1])
            if 'dz' in line:
                resz = float(line.split()[1])
            if 'ftol' in line:
                ftol = float(line.split()[1])

        # Retrieve the force files
        files = sorted(glob.glob(frcfiles))
        zpos = [float('.'.join(x.split('-')[1].split('.')[:2])) for x in files]

        # Figure out the dimensions in x, y and z and the spacing as well
        if files[0][-2:] == 'gz':
            f = gzip.open(files[0], 'r')
        else:
            f = open(files[0], 'r')
        d = f.readlines()
        f.close()
        data = [x for x in d if x[0] != '%']
        nx = numpy.array([int(x.split()[1]) for x in data]).max() + 1
        ny = numpy.array([int(x.split()[2]) for x in data]).max() + 1
        nz = len(zpos)
        tmp = numpy.array(
            sorted(uniquify([float(x.split()[3]) for x in data])))
        dx = (tmp[1:]-tmp[:-1]).mean()
        tmp = numpy.array(
            sorted(uniquify([float(x.split()[4]) for x in data])))
        dy = (tmp[1:]-tmp[:-1]).mean()
        dz = (numpy.array(zpos)[1:]-numpy.array(zpos)[:-1]).mean()

        # Talk to me
        print('Setting Giessibl parameters')

        # Use the Giessibl approach to create frequency shift image (Beilstein J. Nanotechnol. 3:238, 2012)
        Nm2kcalAA = 1.438978
        amplitude = 0.50              # Amplitude of oscillation (in Angstrom)
        # Spring constant of cantilever (in kcal/mol/A/A)
        k_cantilever = 1800*Nm2kcalAA
        # Oscillating frequency of cantilever (in Hz)
        frequency0 = 25.000e3

        # Create the weight function W
        fshiftfac = (frequency0/(2*k_cantilever)) * \
            (2/(numpy.pi*amplitude*amplitude))
        ampcut = (1+(amplitude/dz)) % (1+(amplitude//dz))
        if (ampcut < 0.01):
            amplitude += dz/2   # at -A or A, W -> infinity, thus this precaution
        zosc = numpy.arange(0, amplitude+dz, dz)
        zosc = numpy.concatenate((-zosc[-1:1:-1], zosc))
        W = zosc / numpy.sqrt(abs((amplitude**2)-(zosc**2)))
        W = W[1:-1]   # discard the edges because of W -> infinity as above

        # Build the weight function in the shape of the x and y data
        WXY = numpy.tile(W, [nx, ny, 1])

        # How many frequency shift images can we make (take the width of the oscillation in mind)
        nshifts = len(zpos)-len(W)
        nosc = len(W)

        # Talk to me
        print('Initializing storage arrays')

        # Initialize storage arrays
        FX = numpy.zeros([nx, ny])
        FY = numpy.zeros([nx, ny])
        FZ = numpy.zeros([nx, ny, nosc])
        DX = numpy.zeros([nx, ny])
        DY = numpy.zeros([nx, ny])
        DZ = numpy.zeros([nx, ny])
        ANGLE = numpy.zeros([nx, ny])
        DF = numpy.zeros([nx, ny])
        X = numpy.zeros([nx, ny])
        Y = numpy.zeros([nx, ny])

        # Compute the "real" z's
        realz = numpy.zeros(nz)
        diffz = numpy.zeros(nz)

        # Talk to me
        print('Compute frequency shift (A = %.2f , k = %.1f , f0 = %.3f)' %
              (amplitude, k_cantilever/Nm2kcalAA, frequency0/1000))

        # Number of contour levels in contourf plot
        Nlevels = 60

        # Some "other" settings
        headerfontsize = 6

        # Talk to me
        print('Working...')

        # Make the frequency shift plots
        for pl in range(nshifts):

            # Talk to me
            print('... on step %d' % pl)

            # Load the relevant data
            if (pl == 0):
                for i in range(pl, pl+nosc):
                    # Read file
                    if files[i][-2:] == 'gz':
                        f = gzip.open(files[i], 'r')
                    else:
                        f = open(files[i], 'r')
                    d = f.readlines()
                    f.close()
                    # Skip comment line
                    data = [x for x in d if x[0] != '%']
                    # Read data
                    for d in data:
                        line = d.split()
                        x = int(line[1])  # - 1
                        y = int(line[2])  # - 1
                        FZ[x, y, i-pl] = float(line[8])
                        if i == pl:
                            FX[x, y] = float(line[6])
                            FY[x, y] = float(line[7])
                            DX[x, y] = float(line[9])
                            DY[x, y] = float(line[10])
                            DZ[x, y] = float(line[11])
                            ANGLE[x, y] = float(line[13])
                            X[x, y] = float(line[3])  # - dx
                            Y[x, y] = float(line[4])  # - dy
            else:
                # Read file
                if files[pl][-2:] == 'gz':
                    f = gzip.open(files[pl], 'r')
                else:
                    f = open(files[pl], 'r')
                d = f.readlines()
                f.close()
                # Skip comment line
                data = [x for x in d if x[0] != '%']
                # Read data
                for d in data:
                    line = d.split()
                    x = int(line[1])  # - 1
                    y = int(line[2])  # - 1
                    FX[x, y] = float(line[6])
                    FY[x, y] = float(line[7])
                    DX[x, y] = float(line[9])
                    DY[x, y] = float(line[10])
                    DZ[x, y] = float(line[11])
                    ANGLE[x, y] = float(line[13])
                    X[x, y] = float(line[3])  # - dx
                    Y[x, y] = float(line[4])  # - dy

                # Keep some z-forces
                tmp = deepcopy(FZ)
                FZ[:, :, :-1] = tmp[:, :, 1:]

                # Read file
                kk = pl+nosc-1
                if files[kk][-2:] == 'gz':
                    f = gzip.open(files[kk], 'r')
                else:
                    f = open(files[kk], 'r')
                d = f.readlines()
                f.close()
                # Skip comment line
                data = [x for x in d if x[0] != '%']
                # Read data
                for d in data:
                    line = d.split()
                    x = int(line[1])  # - 1
                    y = int(line[2])  # - 1
                    FZ[x, y, nosc-1] = float(line[8])

            # Compute some thingies
            realz[pl] = zpos[pl]+DZ.mean()
            diffz[pl] = DZ.std()
            DF = -fshiftfac*(FZ*WXY).sum(axis=2)*dz

            ###############################

            fig = plt.figure(0)
            fig.clf()
            ax = fig.add_subplot(1, 1, 1, aspect='equal')
            df = DF[:, :]
            tmp = (df-df.min())/(df.max()-df.min())
            C = ax.contourf(X, Y, tmp, Nlevels, cmap=plt.get_cmap('Blues_r'))
            cbar = fig.colorbar(C, ax=ax, pad=0.02, fraction=0.05,
                                shrink=0.9, spacing='proportional', ticks=[0, 1])
            cbar.ax.set_yticklabels(['min', 'max'])
            # Set axis limits and grid
            ax.grid(True)
            ax.set_xlim([0, dx*nx-dx])
            ax.set_ylim([0, dy*ny-dy])
            # Set some axis/ticks properties
            ax.xaxis.set_major_locator(MultipleLocator(2.0))
            ax.yaxis.set_major_locator(MultipleLocator(2.0))
            ax.set_xlabel(r'x (\u00c5)')
            ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
            ax.set_ylabel(r'y (\u00c5)')
            ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
            ax.title.set_visible(False)
            # Set some text
            txt = r'z = %.3f \u00b1 %.3f \u00c5 | \u0394x = %.3f \u00c5 | \u0394y = %.3f \u00c5 | \u0394z = %.3f \u00c5 | ftol = %.7f | A = %.2f \u00c5 | k = %.1f N/m | f0 = %.2f kHz' % (
                realz[pl], diffz[pl], resx, resy, resz, ftol, amplitude, k_cantilever/Nm2kcalAA, frequency0/1000)
            ax.text(0.015*dx*nx, 1.005*dy*ny, txt,
                    color='k', fontsize=headerfontsize)
            # Save figure
            plt.savefig('deltaf-%06.3f.png' %
                        zpos[pl], dpi=200, bbox_inches='tight', pad_inches=0)

            ############################

            fig = plt.figure(0)
            fig.clf()
            ax = fig.add_subplot(1, 1, 1, aspect='equal')
            angle = ANGLE[:, :]
            tmp = (angle-angle.min())/(angle.max()-angle.min())
            C = ax.contourf(X, Y, tmp, Nlevels, cmap=plt.get_cmap('Greens_r'))
            cbar = fig.colorbar(C, ax=ax, pad=0.02, fraction=0.05,
                                shrink=0.9, spacing='proportional', ticks=[0, 1])
            cbar.ax.set_yticklabels(['min', 'max'])
            # Set axis limits and grid
            ax.grid(True)
            ax.set_xlim([0, dx*nx-dx])
            ax.set_ylim([0, dy*ny-dy])
            # Set some axis/ticks properties
            ax.xaxis.set_major_locator(MultipleLocator(2.0))
            ax.yaxis.set_major_locator(MultipleLocator(2.0))
            ax.set_xlabel(r'x (\u00c5)')
            ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
            ax.set_ylabel(r'y (\u00c5)')
            ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
            ax.title.set_visible(False)
            # Set some text
            txt = r'z = %.3f \u00b1 %.3f \u00c5 | \u0394x = %.3f \u00c5 | \u0394y = %.3f \u00c5 | \u0394z = %.3f \u00c5 | ftol = %.7f | min_angle = %.1f | max_angle = %.1f' % (
                realz[pl], diffz[pl], resx, resy, resz, ftol, angle.min(), angle.max())
            ax.text(0.015*dx*nx, 1.005*dy*ny, txt,
                    color='k', fontsize=headerfontsize)
            # Save figure
            plt.savefig('angle-%06.3f.png' %
                        zpos[pl], dpi=200, bbox_inches='tight', pad_inches=0)

            ###############################

            fig = plt.figure(0)
            fig.clf()
            ax = fig.add_subplot(1, 1, 1, aspect='equal')
            xx = X[:, :]+DX[:, :]
            yy = Y[:, :]+DY[:, :]
            ax.scatter(xx, yy, s=0.2, color='red')
            # Set axis limits and grid
            ax.grid(True)
            ax.set_xlim([0, dx*nx-dx])
            ax.set_ylim([0, dy*ny-dy])
            # Set some axis/ticks properties
            ax.xaxis.set_major_locator(MultipleLocator(2.0))
            ax.yaxis.set_major_locator(MultipleLocator(2.0))
            ax.set_xlabel(r'x (\u00c5)')
            ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
            ax.set_ylabel(r'y (\u00c5)')
            ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
            ax.title.set_visible(False)
            # Set some text
            txt = r'z = %.3f \u00b1 %.3f \u00c5 | \u0394x = %.3f \u00c5 | \u0394y = %.3f \u00c5 | \u0394z = %.3f \u00c5 | ftol = %.7f' % (
                realz[pl], diffz[pl], resx, resy, resz, ftol)
            ax.text(0.015*dx*nx, 1.005*dy*ny, txt,
                    color='k', fontsize=headerfontsize)
            # Save figure
            plt.savefig('displ-%06.3f.png' %
                        zpos[pl], dpi=200, bbox_inches='tight', pad_inches=0)

        '''
		# Talk to me
		print 'Creating animated gifs'
		os.system('convert -resize 800x -loop 0 deltaf-0*.png movie-deltaf.gif')
		os.system('convert -resize 800x -loop 0 angle-0*.png movie-angle.gif')
		os.system('convert -resize 800x -loop 0 displ-0*.png movie-displ.gif')
		'''
        # Talk to me
        print('Done')

    def Initialize(self):

        pass

    def Update(self):
        pass
