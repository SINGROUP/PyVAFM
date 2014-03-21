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

/* ******************************************
 params
 [0] = holderx
 [1] = holdery
 [2] = holderz

 [3] = startingx
 [4] = startingy
 [5] = startingz

 [6] = ztip
 [7] = ztipo

 [8] = ytip
 [9] = ytipo

 [10] = xtip

 [11] = NumberOfModesV
 [12] = NumberOfModesL
vparams

    c.vpparams[0] =Kv
    c.vpparams[1] =Qv
    c.vpparams[2] =Fv

    c.vpparams[3] =Mv
    c.vpparams[4] =Wv
    c.vpparams[5] =Gammav

    c.vpparams[6] =Vv
    c.vpparams[7] =Av
    c.vpparams[8] =Velocityv

    c.vpparams[9]  =Xx
    c.vpparams[10] =Xy
    c.vpparams[11] =Xz



    c.vpparams[12] =Kl
    c.vpparams[13] =Ql
    c.vpparams[14] =Fl

    c.vpparams[15] =Ml
    c.vpparams[16] =Wl
    c.vpparams[17] =Gammal

    c.vpparams[18] =Vl
    c.vpparams[19] =Al
    c.vpparams[20] =Velocityl

    c.vpparams[21] =Xl
    c.vpparams[22] =Yl
    c.vpparams[23] =Zl


 * *****************************************/

int Add_AdvancedCantilever(int owner, int numberofmodesV, int numberofmodesL)
{
	circuit c = NewCircuit();
	c.nI = 6;
	c.nO = 13+numberofmodesL+numberofmodesV;

	c.plen = 11;
	c.params = (double*)calloc(c.plen,sizeof(double));


	c.iplen = 2;
	c.iparams = (int*)calloc(c.iplen,sizeof(int));
	c.iparams[1] = numberofmodesV;
	c.iparams[2] = numberofmodesL;

	
	c.updatef = RunAdvancedCantilever;



    c.vplen = 24;
    c.vpparams = (void**)malloc(c.vplen*sizeof(double*));

    c.vpparams[0] = (double*)calloc(numberofmodesV,sizeof(double));  //Kv
    c.vpparams[1] = (double*)calloc(numberofmodesV,sizeof(double)); 	//Qv
    c.vpparams[2] = (double*)calloc(numberofmodesV,sizeof(double)); 	//Fv

    c.vpparams[3] = (double*)calloc(numberofmodesV,sizeof(double)); 	//Mv
    c.vpparams[4] = (double*)calloc(numberofmodesV,sizeof(double)); 	//Wv
    c.vpparams[5] = (double*)calloc(numberofmodesV,sizeof(double)); 	//Gammav

    c.vpparams[6] = (double*)calloc(numberofmodesV,sizeof(double)); 	//Vv
    c.vpparams[7] = (double*)calloc(numberofmodesV,sizeof(double)); 	//Av
    c.vpparams[8] = (double*)calloc(numberofmodesV,sizeof(double)); 	//Velocityv

    c.vpparams[9] = (double*)calloc(numberofmodesV,sizeof(double)); 	//Xx
    c.vpparams[10] = (double*)calloc(numberofmodesV,sizeof(double)); 	//Xy
    c.vpparams[11] = (double*)calloc(numberofmodesV,sizeof(double)); 	//Xz



    c.vpparams[12] = (double*)calloc(numberofmodesL,sizeof(double));  //Kl
    c.vpparams[13] = (double*)calloc(numberofmodesL,sizeof(double)); 	//Ql
    c.vpparams[14] = (double*)calloc(numberofmodesL,sizeof(double)); 	//Fl

    c.vpparams[15] = (double*)calloc(numberofmodesL,sizeof(double)); 	//Ml
    c.vpparams[16] = (double*)calloc(numberofmodesL,sizeof(double)); 	//Wl
    c.vpparams[17] = (double*)calloc(numberofmodesL,sizeof(double)); 	//Gammal

    c.vpparams[18] = (double*)calloc(numberofmodesL,sizeof(double)); 	//Vl
    c.vpparams[19] = (double*)calloc(numberofmodesL,sizeof(double)); 	//Al
    c.vpparams[20] = (double*)calloc(numberofmodesL,sizeof(double)); 	//Velocityl

    c.vpparams[21] = (double*)calloc(numberofmodesL,sizeof(double)); 	//Xl
    c.vpparams[22] = (double*)calloc(numberofmodesL,sizeof(double)); 	//Yl
    c.vpparams[23] = (double*)calloc(numberofmodesL,sizeof(double)); 	//Zl







	int index = AddToCircuits(c,owner);
	printf("cCore: added advanced cantilever circuit\n");
	return index;
}

int AddK(int c, double *Kpointer)
{

	double *kv = (double*)circuits[c].vpparams[0];
	double *kl = (double*)circuits[c].vpparams[12];

	int numberofmodesV = circuits[c].iparams[1];
	int numberofmodesL = circuits[c].iparams[2];



	for (int i=0;i<numberofmodesV;i++)
	{
		kv[i] = *(Kpointer+i);
		//printf("%f\n", kv[i]);
	}


	for (int i=numberofmodesV;i< (numberofmodesL + numberofmodesV) ;i++)
	{
		kl[i] = *(Kpointer+i);
		//printf("%f\n", kl[i]);
	}

	return c;

}

int AddQ(int c, double *Qpointer)
{

	double *Qv = (double*)circuits[c].vpparams[1];
	double *Ql = (double*)circuits[c].vpparams[13];


	int numberofmodesV = circuits[c].iparams[1];
	int numberofmodesL = circuits[c].iparams[2];




	for (int i=0;i<numberofmodesV;i++)
	{
		Qv[i] = *(Qpointer+i);
		//printf("%f\n", Qv[i]);  /* print first double */
	}


	for (int i=numberofmodesV;i< (numberofmodesL + numberofmodesV) ;i++)
	{
		Ql[i] = *(Qpointer+i);
		//printf("%f\n", Ql[i]);  /* print first double */
	}

	return c;
}

int AddF(int c, double *fpointer)
{

	double *Fv = (double*)circuits[c].vpparams[2];
	double *Fl = (double*)circuits[c].vpparams[14];

	double *Wv = (double*)circuits[c].vpparams[4];
	double *Wl = (double*)circuits[c].vpparams[16];	

	int numberofmodesV = circuits[c].iparams[1];
	int numberofmodesL = circuits[c].iparams[2];




	for (int i=0;i<numberofmodesV;i++)
	{
		Fv[i] = *(fpointer+i);
		Wv[i] = (2*PI* (*(fpointer+i) ) );
		//printf("%f\n", Fv[i]);  /* print first double */
	}


	for (int i=numberofmodesV;i< (numberofmodesL + numberofmodesV) ;i++)
	{
		Fl[i] = *(fpointer+i);
		Wl[i] = (2*PI* (*(fpointer+i) ) );
		//printf("%f\n", Fl[i]);  /* print first double */
	}

	return c;	
}

int AddM(int c, double *Mpointer)
{
		
	double *Mv = (double*)circuits[c].vpparams[2];
	double *Ml = (double*)circuits[c].vpparams[14];


	int numberofmodesV = circuits[c].iparams[1];
	int numberofmodesL = circuits[c].iparams[2];




	for (int i=0;i<numberofmodesV;i++)
	{
		Mv[i] = *(Mpointer+i);
		//printf("%f\n", Mv[i]);  /* print first double */
	}


	for (int i=numberofmodesV;i< (numberofmodesL + numberofmodesV) ;i++)
	{
		Ml[i] = *(Mpointer+i);
		//printf("%f\n", Ml[i]);  /* print first double */
	}

	return c;	
}

int StartingPoint(int c, double *StartingPoint)
{
	circuits[c].params[3] = *(StartingPoint+0); //x
	circuits[c].params[4] = *(StartingPoint+1);	//y
	circuits[c].params[5] = *(StartingPoint+2);	//z
	return c;
}

int setup(int c)
{

}

void RunAdvancedCantilever(circuit *c)
{





}