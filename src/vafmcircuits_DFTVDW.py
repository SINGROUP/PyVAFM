from vafmbase import Circuit
import sys
import numpy as np
import matplotlib.pyplot as plt


class DFTD3(Circuit):

    def __init__(self, machine, name, **keys):

        super(self.__class__, self).__init__(machine, name)

        if 'TipFilename' in list(keys.keys()):
            TipFilename = keys['TipFilename']
        else:
            raise NameError('Missing Tip Filename')

        if 'SurfaceFilename' in list(keys.keys()):
            SurfaceFilename = keys['SurfaceFilename']
        else:
            raise NameError('Missing Surface Filename')

        if 'TipStartingXYZ' in list(keys.keys()):
            TipStartingXYZ = keys['TipStartingXYZ']
        else:
            raise NameError('Missing Tip Starting XYZ ')
        if len(TipStartingXYZ) != 3:
            raise NameError('Tip Starting XYZ must be x y and z')

        DFTD3InstallPath = "./"
        if 'DFTD3InstallPath' in list(keys.keys()):
            DFTD3InstallPath = keys['SurfaceFilename']

        JustBuildXYZFile = False
        if 'JustBuildXYZFile' in list(keys.keys()):
            JustBuildXYZFile = keys['JustBuildXYZFile']

        if 'TipFinalZ' in list(keys.keys()):
            TipFinalZ = keys['TipFinalZ']
        else:
            raise NameError('Missing Tip Final Z Position')

        if 'TipZStep' in list(keys.keys()):
            TipZStep = keys['TipZStep']
        else:
            raise NameError('Missing Tip Z Step')

        if 'OutputFileName' in list(keys.keys()):
            OutputFileName = keys['OutputFileName']
        else:
            raise NameError('Missing Output File Name')

        options = "-func pbe -bj"

        if 'options' in list(keys.keys()):
            options = keys['options']

        if 'TipFinalZ' in list(keys.keys()):
            TipFinalZ = keys['TipFinalZ']
        else:
            raise NameError('Missing Tip Final Z Position')

        RealitiveToSurface = False
        if 'RealitiveToSurface' in list(keys.keys()):
            RealitiveToSurface = keys['RealitiveToSurface']

        Surfacex = []
        Surfacey = []
        Surfacez = []
        SurfaceAtom = []

        Tipx = []
        Tipy = []
        Tipz = []
        TipAtom = []

        with open(TipFilename, 'r') as f:
            next(f)  # skip 1 line
            next(f)  # skip another one.
            for line in f:
                TipAtom.append(line.split()[0])
                Tipx.append(float(line.split()[1]))
                Tipy.append(float(line.split()[2]))
                Tipz.append(float(line.split()[3]))

        NumberofTipAtoms = len(Tipx)

        with open(SurfaceFilename, 'r') as f:
            next(f)  # skip 1 line
            next(f)  # skip another one.
            for line in f:
                SurfaceAtom.append(line.split()[0])
                Surfacex.append(float(line.split()[1]))
                Surfacey.append(float(line.split()[2]))
                Surfacez.append(float(line.split()[3]))

        SurfaceHeight = max(Surfacez)
        if 'SurfaceHeight' in list(keys.keys()):
            SurfaceHeight = keys['SurfaceHeight']

        NumberofSurfaceAtoms = len(Surfacex)

        # Find bottom atom
        LowestAtomIndex = Tipz.index(min(Tipz))

        # Adjust tip position to be above 0
        Shiftxyz = [Tipx[LowestAtomIndex],
                    Tipy[LowestAtomIndex], Tipz[LowestAtomIndex]]
        for i, j in enumerate(Tipx):

            Tipx[i] = Tipx[i] - Shiftxyz[0] + TipStartingXYZ[0]
            Tipy[i] = Tipy[i] - Shiftxyz[1] + TipStartingXYZ[1]
            Tipz[i] = Tipz[i] - Shiftxyz[2] + TipStartingXYZ[2]

        # Write all XYZ and Bash files
        fBash = open('Temp.sh', 'w')
        z = 0
        FileCounter = 0
        TipZArray = []

        while z <= (TipFinalZ-TipStartingXYZ[2]):
            FileCounter + FileCounter + 1

            for i, j in enumerate(Tipx):
                if z > 0:
                    Tipz[i] = Tipz[i]+TipZStep

            TempAtoms = SurfaceAtom + TipAtom
            Tempx = Surfacex + Tipx
            Tempy = Surfacey + Tipy
            Tempz = Surfacez + Tipz

            f = open('z='+str(TipStartingXYZ[2]+z)+'.xyz', 'w')
            f.write(str(NumberofTipAtoms+NumberofSurfaceAtoms)+"\n")
            f.write("\n")

            for i in range(0, NumberofTipAtoms+NumberofSurfaceAtoms):

                f.write(str(TempAtoms[i]) + " "*(2-len(TempAtoms[i])) + " "*(10+(12-len(str('{0:.10f}'.format(Tempx[i]))))) + str('{0:.10f}'.format(Tempx[i])) + " "*(
                    10+(12-len(str('{0:.10f}'.format(Tempy[i]))))) + str('{0:.10f}'.format(Tempy[i])) + " "*10 + str('{0:.10f}'.format(Tempz[i])) + "\n")

            f.close()
            TipZArray.append(TipStartingXYZ[2]+z)
            fBash.write(str(DFTD3InstallPath)+"dftd3 " + 'z=' + str(
                TipStartingXYZ[2]+z) + ".xyz" + " " + options + " >"+str(TipStartingXYZ[2]+z)+".txt \n")

            z = z + TipZStep

            if JustBuildXYZFile == True:
                print("XYZ File Written for starting height")
                sys.exit()

        fBash.close()
        print("Bash script and xyz files written")

        import os
        os.system("sh Temp.sh")

        Energy = []

        for z in TipZArray:
            f = open(str(z)+".txt")
            for line in f:
                if len(line.split()) > 0:
                    if line.split()[0] == "Edisp":
                        Energy.append(float(line.split()[3])*27.21138505)

        os.system("rm *.txt")

        for i in TipZArray:
            os.system("rm "+"z="+str(i)+".xyz")

        Force = np.diff(Energy)*-1
        del(TipZArray[-1])

        FileO = open(OutputFileName, 'w')

        if RealitiveToSurface == True:
            for i in range(0, len(TipZArray)):
                FileO.write(str(TipZArray[i]-SurfaceHeight) +
                            " "+str(Force[i]) + " "+str(Energy[i])+"\n")

        if RealitiveToSurface == False:
            for i in range(0, len(TipZArray)):
                FileO.write(str(TipZArray[i])+" " +
                            str(Force[i]) + " "+str(Energy[i])+"\n")

        FileO.close()

    def Initialize(self):

        pass

    def Update(self):
        pass
