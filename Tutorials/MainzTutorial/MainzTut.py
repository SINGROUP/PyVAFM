#!/usr/bin/env python
from customs import *
from vafmcircuits import Machine
import sys
sys.path.append('/home/vafm/src')

# Force Field units are nm and nN
# Variables
f0 =
Az =  # nm
Q =
k =  # N/m


# Adding Circuits Section 1
##############################################################################
machine = Machine(machine=None, name='machine', dt=1e-5)
scanner = machine.AddCircuit(
    type='Scanner', name='scan', Process=machine, pushed=True)

inter = machine.AddCircuit(
    type='i3Dlin', name='inter', components=1, pushed=True)
inter.Configure(steps=[0.0508, 0.0616625, 0.005], npoints=[16, 8, 200])
inter.Configure(pbc=[True, True, False])
# the values here are KJ/mol/nm. this factor brings them to nN
inter.Configure(ForceMultiplier=0.00166)
inter.ReadData('ForceField.dat')

canti = machine.AddCircuit(
    type='Cantilever', name='canti', startingz=Az, Q=Q, k=k, f0=f0, pushed=True)

machine.AddCircuit(type="Machine", name='amp', fcut=100,
                   assembly=aAMPD, pushed=True)


##########################
# Add PI Circuit Here

##########################


##########################
# Add PLL here

##########################


machine.AddCircuit(type='waver', name='testwave', freq=f0, amp=1)


machine.AddCircuit(type='opMul', name='exc', pushed=True)
machine.AddCircuit(type='opMul', name='inv', in2=-1, pushed=True)
##############################################################################


# Connect Circuits Section 2
##############################################################################
# pll setup


machine.Connect("scan.x", "inter.x")
machine.Connect("scan.y", "inter.y")


machine.Connect("scan.z", "canti.holderz")
machine.Connect("canti.zabs", "inter.z")


# Force to cantilever
machine.Connect("inter.F1", "canti.fz")

# exciter to canti
machine.Connect('exc.out', 'canti.exciter')


# machine.Connect('testwave.cos','pll.signal1')
##########################
# Add Connections here


##########################

##############################################################################


# Setup Output Circuits Section 3
##############################################################################
out1 = machine.AddCircuit(type='output', name='output',
                          file='debug.dat', dump=1)
out1.Register('global.time', "scan.x", 'canti.zabs',
              'amp.amp', 'agc.out', "pll.df")


# Imaging output
imager = machine.AddCircuit(
    type='output', name='image', file='Image.dat', dump=0)
imager.Register("scan.x", "scan.y", "pll.df")

machine.Connect("scan.record", "image.record")
##############################################################################


# Cantilever Movement Section 4
##############################################################################
scanner.Place(x=0, y=0, z=1.5)

##########################
# Pll Testing Commands
'''
scanner.Place(x=0,y=0,z=1.5)
machine.Wait(0.5)
machine.circuits['testwave'].I['freq'].Set(f0+50)
machine.Wait(0.5)
machine.circuits['testwave'].I['freq'].Set(f0-300)
machine.Wait(0.5)
machine.circuits['testwave'].I['freq'].Set(f0+800)
machine.Wait(0.5)
'''
##########################


##########################
# Scripting Commands


##########################

##############################################################################
