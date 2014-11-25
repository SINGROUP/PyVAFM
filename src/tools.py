import math

#Function for interpolating a 3d array with pbc
def interpolate(Array,step,x,y,z):

	#Find pos - pbc
	n = [len(Array)-1,len(Array[0])-1,len(Array[0][0])-1]
	#print x,y,z
	x -= math.floor(x/( n[0]*step[0] )) * n[0]*step[0]
	y -= math.floor(y/( n[1]*step[1] )) * n[1]*step[1]
	z -= math.floor(z/( n[2]*step[2] )) * n[2]*step[2]


	#Find voxel indexs
	x0 = int (math.floor(x/step[0]))
	y0 = int (math.floor(y/step[1]))
	z0 = int (math.floor(z/step[2]))


	
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