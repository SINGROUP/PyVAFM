from scipy.interpolate import griddata
import math

def Transform(size,dx,dy,dz,Vx,Vy,Vz,x,y,z):
		
	#Transfer it into the correct frame
	pos = [0,0,0]
	fracx = x*dx/size[0]
	fracy = y*dy/size[1]
	fracz = z*dz/size[2]

					

	pos[0] = fracx * Vx[0]
	pos[1] = fracx * Vx[1]
	pos[2] = fracx * Vx[2]

							
	pos[0] += fracy * Vy[0]
	pos[1] += fracy * Vy[1]
	pos[2] += fracy * Vy[2]

							
	pos[0] += fracz * Vz[0]
	pos[1] += fracz * Vz[1]
	pos[2] += fracz * Vz[2]

	return pos