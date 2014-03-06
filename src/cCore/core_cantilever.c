/**********************************************************
Cantilever circuits definitions.
*********************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef CORECANTILEVER
#include "core_cantilever.h"
#endif



/* ******************************************
 * inputs[0] = holderz
 * inputs[1] = fz
 * inputs[2] = exciterforce
 * outputs[0] = ztip - relative to canti
 * outputs[1] = zabs
 * outputs[2] = vz
 * 
 * params[0] = reduced gamma = 0.5*(2*PI*F*dt)/Q
 * params[1] = reduced mass = dt^2/mass = (2*PI*F*dt)^2/ks
 * params[2] = z - of the tip relative to cantilever
 * params[3] = v
 * params[4] = a
 * params[5] = cantioffset z
 * params[6] = reduced omega
 * *****************************************/
int Add_Cantilever(int owner, double Q, double k, double M, double f0, double startingz, double cantiz) {

	double W = 2*PI*f0*dt; //angular pulse times dt
	double gamma = 0.5*(W/Q);

	//the M is actually dt^2/Mass
	if (M==0) {
		printf("cCore: cantilever mass not given, calculating from K and omega\n");
		M=(W*W)/k;
	}

	circuit c = NewCircuit();
	c.nI = 3;
	c.nO = 3;

	c.plen = 7;
	c.params = (double*)calloc(c.plen,sizeof(double));
	c.params[0] = gamma;
	c.params[1] = M;
	c.params[2] = startingz;
	c.params[5] = cantiz;
	c.params[6] = W;
	
	c.updatef = RunCantilever;

	int index = AddToCircuits(c,owner);
	printf("cCore: added basic cantilever circuit\n");
	return index;

}


void RunCantilever(circuit *c) {
	
	//update tip z
	c->params[2] += c->params[3]*dt*(1.0-c->params[0]) + 0.5*c->params[4]*dt;
	//update velocity - half step
	c->params[3] = c->params[3]*(1.0-c->params[0]) + 0.5*c->params[4];
	
	//output the ztip - relative to the cantilever
	GlobalBuffers[c->outputs[0]] = c->params[2];
	//output the vztip
	GlobalBuffers[c->outputs[2]] = c->params[3];
	
	//apply cantilever fixed offset = holderz + offset + ztip
	GlobalBuffers[c->outputs[1]] = GlobalSignals[c->inputs[0]] + c->params[5] + c->params[2]; 
	//push the absolute position buffer
	GlobalSignals[c->outputs[1]] = GlobalBuffers[c->outputs[1]];
	
	//second part of the update
	//in principle here the forces should be updated!
	//MAYBE LEAPFROG IS MORE CORRECT!
	double az = GlobalSignals[c->inputs[1]] + GlobalSignals[c->inputs[2]]; //total force
	
	c->params[4] = az*c->params[1] - c->params[2]*c->params[6]*c->params[6];
	c->params[4] /= dt;
	c->params[3] = c->params[3]*(1.0-c->params[0]) + 0.5*c->params[4]; //update v (half step)

}



int Add_AdvancedCantilever(int owner, int numberofmodesV, int numberofmodesL)
{
	circuit c = NewCircuit();
	c.nI = 6;
	c.nO = 8+numberofmodesL+numberofmodesV;


	c.plen = 7;
	c.params = (double*)calloc(c.plen,sizeof(double));

	
	c.updatef = RunAdvancedCantilever;

	int index = AddToCircuits(c,owner);
	printf("cCore: added advanced cantilever circuit\n");
	return index;
}

int AddK(double *Kpointer)
{
	printf("%f\n", *(Kpointer+2));  /* print first double */
}

int AddQ(double *Qpointer)
{
	printf("%f\n", *(Qpointer+2) );  /* print first double */
}

int AddF(double *fpointer)
{
	printf("%f\n", *(fpointer+2) );  /* print first double */
}

int AddM(double *Mpointer)
{
	printf("%f\n", *(Mpointer+2) );  /* print first double */
}

int StartingPoint(double *StartingPoint)
{
	printf("%f\n", *(StartingPoint+2) );  /* print first double */
}


void RunAdvancedCantilever(circuit *c)
{

}