/**********************************************************
Resonance Shear Apparatus definitions.
*********************************************************/
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef CORERSA
#include "core_rsa.h"
#endif

/******************************************************
 * inputs[0]	= exciter
 * inputs[1]	= viscosity
 * inputs[2]	= friction coeff
 * output[0]	= xcm
 * output[1]	= ycm
 * output[2]	= theta
 * output[3]	= x2
 * params[0-2]	= 1/M1, 1/M2, 1/Mrot
 * params[3-5]	= K1, K1z, K2
 * params[6-8]	= gamma1, gamma2, gammaRot
 * params[9-11]	= springx, springy, forcepoint(y)
 * params[12-15]= xcm,ycm,angle,x2
 * params[16-19]= vxcm,vycm,vangle,vx2
 * 
 * iparams[0] 	= components
 * iparams[1-3]	= number of points nx ny nz
 * iparams[4] 	= size of field (1 component) nx*ny*nz
 * iparams[5] 	= size of zy plane (1 component) ny*nz
 * iparams[6-8]	= periodic 0|1 along each direction
 * ***************************************************/
int Add_RSA( int owner ) {

    //printf("%i \n",xsize);

    circuit c = NewCircuit();
    c.nI = 3;
    c.nO = 4;

    /*c.iplen = 9;
    c.iparams = (int*)calloc(c.iplen,sizeof(int));
    c.iparams[0] = components;*/

    c.plen = 20;
    c.params = (double*)calloc(c.plen,sizeof(double));
    
    c.updatef = RSA; //this is the default scanner update function
    int index = AddToCircuits(c,owner);
    printf("cCore: RSA initialised\n");
    return index;
	
}

int RSA_SetMasses(int c, double m1, double m2, double mi) {
	
	circuits[c].params[0] = 1.0/m1;
	circuits[c].params[1] = 1.0/m2;
	circuits[c].params[2] = 1.0/mi;
	
	printf("cCore: RSA masses set: %lf %lf %lf \n",circuits[c].params[0],
		circuits[c].params[1],circuits[c].params[2]);
	
	return 0;
}
int RSA_SetSprings(int c, double k1, double k1z, double k2) {
	
	circuits[c].params[3] = k1;
	circuits[c].params[4] = k1z;
	circuits[c].params[5] = k2;
	printf("cCore: RSA springs set: %lf %lf %lf \n",circuits[c].params[3],
		circuits[c].params[4],circuits[c].params[5]);
	return 0;
}
int RSA_SetGammas(int c, double g1, double g2, double gr) {
	
	circuits[c].params[6] = g1;
	circuits[c].params[7] = g2;
	circuits[c].params[8] = gr;
	
	printf("cCore: RSA gammas set: %lf %lf %lf \n",circuits[c].params[6],
		circuits[c].params[7],circuits[c].params[8]);
	
	return 0;
}
int RSA_SetPoints(int c, double sx, double sy, double fp) {
	
	circuits[c].params[ 9] = sx;
	circuits[c].params[10] = sy;
	circuits[c].params[11] = fp;
	
	printf("cCore: RSA force points set: %lf %lf %lf \n",circuits[c].params[9],
		circuits[c].params[10],circuits[c].params[11]);
	
	return 0;
}

void RSA (circuit* c) {
	
	double eta = GlobalSignals[c->inputs[1]];
	double torq = GlobalSignals[c->inputs[0]];
	
	for(int i=0; i<4; i++)
		c->params[12+i] += c->params[16+i]*dt;
	
 	// compute forces **************************************************
	double theta = c->params[14];
	//compute the correct position
	double x = c->params[9]*cos(theta) - c->params[10]*sin(theta);
	double y = c->params[9]*sin(theta) + c->params[10]*cos(theta);
	x += c->params[12]; y += c->params[13]; //absolute position of the spring attachement point
	
	double tmpfx = -c->params[3] * (x - c->params[9]);
	double tmpfy = -c->params[4] * (y - c->params[10]);
	torq += (x - c->params[12])*tmpfy -  (y- c->params[13])*tmpfx;
	double forcex = tmpfx, forcey = tmpfy;
	//and for the second spring
	x = -c->params[9]*cos(theta) - c->params[10]*sin(theta);
	y = -c->params[9]*sin(theta) + c->params[10]*cos(theta);
	x += c->params[12]; y += c->params[13]; //absolute position of the spring attachement point
	
	tmpfx = -c->params[3] * (x + c->params[9]);
	tmpfy = -c->params[4] * (y - c->params[10]);
	torq += (x - c->params[12])*tmpfy -  (y- c->params[13])*tmpfx;
	forcex += tmpfx; forcey += tmpfy;
	
	double force2 = -c->params[5] * c->params[15]; //lower spring
	
	//******************************************************************
	
 	eta = -eta*(c->params[16] + (-c->params[11])*c->params[18]*cos(theta)-c->params[19]);
 	forcex += eta; 
 	force2 -= eta;
	torq += 0-(c->params[11]*cos(theta)*eta); //torq += 0-(c->params[11]*cos(theta)*mu);
	//update speeds
	c->params[16] = (c->params[16] + forcex*dt*c->params[0])/(1.0 + c->params[6]*dt*c->params[0]);
	c->params[17] = (c->params[17] + forcey*dt*c->params[0])/(1.0 + c->params[6]*dt*c->params[0]);
	c->params[18] = (c->params[18] + torq  *dt*c->params[2])/(1.0 + c->params[8]*dt*c->params[2]);
	c->params[19] = (c->params[19] + force2*dt*c->params[1])/(1.0 + c->params[7]*dt*c->params[1]);

	
	GlobalBuffers[c->outputs[0]] = c->params[12];
	GlobalBuffers[c->outputs[1]] = c->params[13];
	GlobalBuffers[c->outputs[2]] = c->params[14];
	GlobalBuffers[c->outputs[3]] = c->params[15];
	
}







