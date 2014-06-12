# -*- coding:utf-8 -*-
import math
from vafmbase import Circuit
from ctypes import *

## \brief Scanner circuit.
#
#
# \image html scanner.png "schema"
# The scanner circuit is designed to move the cantilever over time.
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Initialisation \b Commands:
#	- Place(x=float,y=float,z=float) = Place the scanner at a given location.
#	- Move(x=float,y=float,z=float, v=float) = Move the scanner by a give vector at a given speed.
#	- MoveTo(x=float,y=float,z=float, v=float) = Move the scanner to a given postion at a given speed.
#	- MoveRecord(x=float,y=float,z=float, v=float, points=integer) = same as Move command except will only record a set number of points
#	- Direction(x=integer,y=integer,z=integer) = Set the direction of the fast scan using a tyical unit vector format.
#	- ScanArea() = Start the auto scan (this should be set up as shown in the tutorials)
#
# \b Variables
#	- Recorder = output circuit to be used with the ScanArea function
#	- BlankLines True|False = To dictate if it will include blank lines in the output file, so the file will work with gnuplots pm3d.
#	- Resolution = A vector of the scan resoloution eg: [30,60] woudl mean 30 lines in slow direction and 60 in fast direction
#
# \b Output \b channels:
# 	- \a x = x coordinate value.
# 	- \a y = y coordinate value.
# 	- \a z = z coordinate value.
#	- \a record = Will output 1 when the scanner wants to output a value.
#
#\b Examples:
# \code{.py}
#	scanner = machine.AddCircuit(type='Scanner',name='scan', pushed=True )
# 	scanner.Place(x=0,y=0,z=0)
# 	scanner.MoveTo(x=1,y=1,z=1,v=1)
# \endcode
#


class Scanner(Circuit):

	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )

		self.AddOutput("x")
		self.AddOutput("y")
		self.AddOutput("z")
		self.AddOutput("record")

		self._fastscan = [1,0,0]
		self._slowscan = [0,1,0]
		self._landscan = [0,0,1]
		
		## Size of the image along fast and slow scan directions
		#
		self.ImageSize = [1,1]
		
		## Resolution of the image
		#
		self.Resolution = [20,7]
		
		## Fastscan speed
		#
		self.FastSpeed = 1
		## Slowscan speed
		#
		self.SlowSpeed = 1
		## Reference to the dedicated output circuit
		#
		self.Recorder = None
		## Insert blank line in the dedicated output
		#
		self.BlankLines = False
		
		Circuit.cCore.Scanner_Place.argtypes = [c_int, c_double, c_double, c_double]
		self.GetParams = Circuit.cCore.ScannerParams
		self.GetParams.restype = POINTER(c_double)
		
		self.cCoreID = Circuit.cCore.Scanner( self.machine.cCoreID )
		self.SetInputs(**keys)




	def Move(self, x = 0, y = 0, z = 0, v = 1): #default arguments, make the input lighter
		steps = Circuit.cCore.Scanner_Move(self.cCoreID, c_double(x), c_double(y) ,c_double(z),c_double(v) )
		self.machine.main.WaitSteps(steps)
		print "Scanner moved by " +str(x) + "," + str(y)+ "," + str(z)

	def Place(self,**kw): #all parameters required
		
		#finds out where the scanner is by asking cCore
		params = self.GetParams(self.cCoreID);
		x = params[0]
		y = params[1]
		z = params[2]
		print "original place: ",x,y,z
		
		if 'x' in kw.keys():
			x = kw['x']
		if 'y' in kw.keys():
			y = kw['y']
		if 'z' in kw.keys():
			z = kw['z']
		
		steps = Circuit.cCore.Scanner_Place(self.cCoreID, c_double(x), c_double(y), c_double(z))
		self.machine.main.WaitSteps(1)
		print "Scanner Placed at ", x, y, z

	def MoveTo(self,**kw):
		
		#finds out where the scanner is by asking cCore
		params = self.GetParams(self.cCoreID);
		x = params[0]
		y = params[1]
		z = params[2]
		v = 0
		
		if "x" in kw.keys(): x = float(kw["x"])
		if "y" in kw.keys(): y = float(kw["y"])
		if "z" in kw.keys(): z = float(kw["z"])

		if ("v" in kw.keys()):
			v = float(kw["v"])
		else:
			raise NameError ("ERROR! Scanner MoveTo requires v.")

		steps = Circuit.cCore.Scanner_MoveTo(self.cCoreID, c_double(x), c_double(y), c_double(z), c_double(v))
		self.machine.main.WaitSteps(steps)                
		print "Scanner moved to " +str(x) + "," + str(y)+ "," + str(z)

	#def Scan(self,x,y,z,v,points):
		#steps = Circuit.cCore.Scanner_Scan(self.cCoreID, c_double(x), c_double(y) ,c_double(z),c_double(v),points )
		#Machine.main.Wait(steps*self.machine.dt)                
		#print "Scanner scanned to " +str(x) + "," + str(y)+ "," + str(z)

	## Used to set the fast scan direction
	#
	def FastScan(self, direction):
		
		if len(direction) != 3:
			raise ValueError("ERROR! Invalid fast scan direction!")
		
		x = direction[0]
		y = direction[1]
		z = direction[2]
		n = math.sqrt(x*x + y*y + z*z)
		if n == 0:
			raise ValueError("ERROR! Zero fast scan direction -!")
		self._fastscan[0] = x/n
		self._fastscan[1] = y/n
		self._fastscan[2] = z/n
		print "fastscan direction set: ",self._fastscan
		
	## Used to set the slow scan direction
	#
	def SlowScan(self, direction):
		
		if len(direction) != 3:
			raise ValueError("ERROR! Invalid slow scan direction!")
		
		x = direction[0]
		y = direction[1]
		z = direction[2]
		n = math.sqrt(x*x + y*y + z*z)
		if n == 0:
			raise ValueError("ERROR! Zero slow scan direction -!")
		self._slowscan[0] = x/n
		self._slowscan[1] = y/n
		self._slowscan[2] = z/n
		
		print "slowscan direction set: ",self._slowscan

	## Set fast and/or slow scan directions
	#
	def Direction(self, **kw):
		
		if "fast" in kw.keys():
			self.FastScan(kw["fast"])
		if "slow" in kw.keys():
			self.SlowScan(kw["slow"])
		

	## Set the size of the image along the fast and slow scan directions
	def ImageArea(self, fast, slow):
		
		self.ImageSize[0] = fast
		self.ImageSize[1] = slow

	def ScanArea(self):
		
		print "Scanning area..."
		
		params = self.GetParams(self.cCoreID);
		x = params[0]; y = params[1]; z = params[2]
		x0 = [x,y,z]
		
		#compute the movement along fast and slow scan
		dfast = [0,0,0]
		dslow = [0,0,0]
		for i in range(3):
			dfast[i] = c_double(self._fastscan[i] * self.ImageSize[0])
			dslow[i] = self._slowscan[i] * self.ImageSize[1] / float(self.Resolution[1])
		
		#print dfast,dslow
		
		#loop for each scanline to take
		for linenum in range(1,self.Resolution[1]+1):
			
			print "PY Scanner: starting line number "+str(linenum) + "..."
			
			#move to the end of fast scanline
			steps = Circuit.cCore.Scanner_Move_Record(self.cCoreID, dfast[0],dfast[1],dfast[2],
				c_double(self.FastSpeed), c_int(self.Resolution[0]) )
			self.machine.main.WaitSteps(steps)
			
			print "PY Scanner: done. Repositioning..."
			
			if self.BlankLines == True and self.Recorder != None:
				self.Recorder.DumpMessage("")
			
			
			#move to initial pos + step along slowscan
			repos = [c_double(x0[i]+linenum*dslow[i]) for i in range(3)]
			#print "repositioning: ",repos
			steps = Circuit.cCore.Scanner_MoveTo(self.cCoreID, repos[0], repos[1], repos[2],
				c_double(self.SlowSpeed))
			self.machine.main.WaitSteps(steps)
			print "PY Scanner: done."
			
		
		#now go back to the original position
		print "PY Scanner: Moving to starting location..."
		repos = [c_double(x0[i]) for i in range(3)]
		steps = Circuit.cCore.Scanner_MoveTo(self.cCoreID, repos[0], repos[1], repos[2],
				c_double(self.SlowSpeed))
		self.machine.main.WaitSteps(steps)
		
		print "done!"


	def MoveRecord(self, **kw):
		#finds out where the scanner is by asking cCore
		params = self.GetParams(self.cCoreID);
		x = params[0]
		y = params[1]
		z = params[2]
		v = 1
		npts=0
		if "x" in kw.keys(): x = float(kw["x"])
		if "y" in kw.keys(): y = float(kw["y"])
		if "z" in kw.keys(): z = float(kw["z"])
		if ("v" in kw.keys()):
			v = float(kw["v"])
		else:
			raise NameError ("ERROR! Scanner MoveRecord requires v.")
		if ("points" in kw.keys()):
			npts = int(kw["points"])
		else:
			raise NameError ("ERROR! Scanner MoveRecord requires number of points.")


		steps = Circuit.cCore.Scanner_Move_Record(self.cCoreID, c_double(x), c_double(y), c_double(z), c_double(v), c_int(npts)) 
		self.machine.main.WaitSteps(steps)                
		print "Scanner moved by " +str(x) + "," + str(y)+ "," + str(z)


