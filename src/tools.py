import math
import sys
#Function for interpolating a 3d array with pbc
def interpolate(Array,step,x,y,z):
	if z >= (step[2])*len(Array[0][0]) - step[2]:

		return 0

	if z < 0:
		print "CRASHED INTO SURFACE"
		sys.exit()		
	
	#Find pos - pbc
	n = [len(Array)-1,len(Array[0])-1,len(Array[0][0])-1]

	#print x,y,z
	#+1 here

	#	 adjust for PBC
	x -= math.floor(x/( (n[0])*step[0] )) * (n[0]+1)*step[0]
	
	y -= math.floor(y/( (n[1])*step[1] )) * (n[1]+1)*step[1]
	z -= math.floor(z/( (n[2])*step[2] )) * (n[2]+1)*step[2]


	#Find voxel indexs
	x0 = int ( math.floor(int(round(x/step[0],3))))
	y0 = int ( math.floor(int(round(y/step[1],3))))
	z0 = int ( math.floor(int(round(z/step[2],3))))


	'''
	y0 = int (math.floor(y/step[1])) 
	z0 = int (math.floor(z/step[2])) 
	'''

	

	
	if x0 == n[0]:
		x0 = 0
	
	if y0 == n[1]:
		y0 = 0
	
	if z0 == n[2]:
		z0 = 0



	x1 = x0 + 1
	y1 = y0 + 1
	z1 = z0 + 1



	#Find xd,yd,zd
	xd = (x - x0*step[0] ) / (x1*step[0] - x0*step[0] )
	yd = (y - y0*step[1] ) / (y1*step[1] - y0*step[1] )
	zd = (z - z0*step[2] ) / (z1*step[2] - z0*step[2] )

	c00 = Array[x0][y0][z0] * (1-xd) + Array[x1][y0][z0] * xd
	c10 = Array[x0][y1][z0] * (1-xd) + Array[x1][y1][z0] * xd
	c01 = Array[x0][y0][z1] * (1-xd) + Array[x1][y0][z1] * xd
	c11 = Array[x0][y1][z1] * (1-xd) + Array[x1][y1][z1] * xd


	c0 = c00*(1-yd) + c10*yd
	c1 = c01*(1-yd) + c11*yd

	c = c0*(1-zd) + c1*zd



	return c


#The recipe gives simple implementation of a Discrete Proportional-Integral-Derivative (PID) controller. PID controller gives output value for error between desired reference input and measurement feedback to minimize error value.
#More information: http://en.wikipedia.org/wiki/PID_controller
#
#cnr437@gmail.com
#
#######	Example	#########
#
#p=PID(3.0,0.4,1.2)
#p.setPoint(5.0)
#while True:
#     pid = p.update(measurement_value)
#
#


class PID:
	"""
	Discrete PID control
	"""

	def __init__(self, P=2.0, I=0.0, D=1.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500):

		self.Kp=P
		self.Ki=I
		self.Kd=D
		self.Derivator=Derivator
		self.Integrator=Integrator
		self.Integrator_max=Integrator_max
		self.Integrator_min=Integrator_min

		self.set_point=0.0
		self.error=0.0

	def update(self,current_value):
		"""
		Calculate PID output value for given reference input and feedback
		"""

		self.error = self.set_point - current_value

		self.P_value = self.Kp * self.error
		self.D_value = self.Kd * ( self.error - self.Derivator)
		self.Derivator = self.error

		self.Integrator = self.Integrator + self.error

		if self.Integrator > self.Integrator_max:
			self.Integrator = self.Integrator_max
		elif self.Integrator < self.Integrator_min:
			self.Integrator = self.Integrator_min

		self.I_value = self.Integrator * self.Ki

		PID = self.P_value + self.I_value + self.D_value

		return PID

	def setPoint(self,set_point):
		"""
		Initilize the setpoint of PID
		"""
		self.set_point = set_point
		self.Integrator=0
		self.Derivator=0

	def setIntegrator(self, Integrator):
		self.Integrator = Integrator

	def setDerivator(self, Derivator):
		self.Derivator = Derivator

	def setKp(self,P):
		self.Kp=P

	def setKi(self,I):
		self.Ki=I

	def setKd(self,D):
		self.Kd=D

	def getPoint(self):
		return self.set_point

	def getError(self):
		return self.error

	def getIntegrator(self):
		return self.Integrator

	def getDerivator(self):
		return self.Derivator
