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
 * params[7] = vold
 * params[8] = aold
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

	c.plen = 10;
	c.params = (double*)calloc(c.plen,sizeof(double));
	c.params[0] = gamma;
	c.params[1] = M;
	c.params[2] = startingz;
	c.params[5] = cantiz;
	c.params[6] = W;
	c.params[7] = 0;
	c.params[8] = 0;	
	c.params[9] = 0;
	c.updatef = RunCantilever;

	int index = AddToCircuits(c,owner);
	printf("cCore: added basic cantilever circuit\n");
	return index;

}


void RunCantilever(circuit *c) {

	
		//second part of the update
	//in principle here the forces should be updated!
	//MAYBE LEAPFROG IS MORE CORRECT!

	
	if (c->params[9] == 1){


	double az = GlobalSignals[c->inputs[1]] + GlobalSignals[c->inputs[2]]; //total force
	
	c->params[4] = az*c->params[1] - c->params[2]*c->params[6]*c->params[6];
	c->params[4] /= dt;
	c->params[3] = c->params[3]*(1.0-c->params[0]) + 0.5*c->params[4]; //update v (half step 2/2)
	}
	//Verlet End


	//Verlet Start
	//update tip z
	c->params[2] += c->params[3]*dt*(1.0-c->params[0]) + 0.5*c->params[4]*dt;
	//update velocity - half step (1/2)
	c->params[3] = c->params[3]*(1.0-c->params[0]) + 0.5*c->params[4];



	c->params[9] = 1;

	//output the ztip - relative to the cantilever
	GlobalBuffers[c->outputs[0]] = c->params[2];
	//output the vztip
	GlobalBuffers[c->outputs[2]] = c->params[3];
	
	//apply cantilever fixed offset = holderz + offset + ztip
	GlobalBuffers[c->outputs[1]] = GlobalSignals[c->inputs[0]] + c->params[5] + c->params[2]; 
	//push the absolute position buffer
	GlobalSignals[c->outputs[1]] = GlobalBuffers[c->outputs[1]];

/*
	
	//second part of the update
	//in principle here the forces should be updated!
	//MAYBE LEAPFROG IS MORE CORRECT!
	double az = GlobalSignals[c->inputs[1]] + GlobalSignals[c->inputs[2]]; //total force
	
	c->params[4] = az*c->params[1] - c->params[2]*c->params[6]*c->params[6];
	c->params[4] /= dt;
	c->params[3] = c->params[3]*(1.0-c->params[0]) + 0.5*c->params[4]; //update v (half step)
*/	
 

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

 iparams
 [0] = NumberOfModesV
 [1] = NumberOfModesL
 [2] = first run check 

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

    c.vpparams[9]  =Xv
    c.vpparams[10] =Xv
    c.vpparams[11] =Xv


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
	c.nI = 11;
	c.nO = 9+numberofmodesL*2+numberofmodesV*2;

	c.plen = 11;
	c.params = (double*)calloc(c.plen,sizeof(double));

	// check is for first run set up
	int check = 0;
	c.iplen = 3;
	c.iparams = (int*)calloc(c.iplen,sizeof(int));
	c.iparams[0] = numberofmodesV;
	c.iparams[1] = numberofmodesL;
	c.iparams[2] = check;

	
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

    c.vpparams[9] = (double*)calloc(numberofmodesV,sizeof(double)); 	//Xv
    c.vpparams[10] = (double*)calloc(numberofmodesV,sizeof(double)); 	//Xv
    c.vpparams[11] = (double*)calloc(numberofmodesV,sizeof(double)); 	//Xv



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

	int numberofmodesV = circuits[c].iparams[0];
	int numberofmodesL = circuits[c].iparams[1];


	
	for (int i=0;i<numberofmodesV;i++)
	{
		kv[i] = *(Kpointer+i);
		//printf("%f ", kv[i]);
	}

	int j=0;	
	for (int i=numberofmodesV;i< (numberofmodesL + numberofmodesV) ;i++)
	{
		kl[j] = *(Kpointer+i);
		//printf("%f ", kl[j]);
		j++;
	}
	

	//printf("\n");
}

int AddQ(int c, double *Qpointer)
{

	double *Qv = (double*)circuits[c].vpparams[1];
	double *Ql = (double*)circuits[c].vpparams[13];


	int numberofmodesV = circuits[c].iparams[0];
	int numberofmodesL = circuits[c].iparams[1];




	for (int i=0;i<numberofmodesV;i++)
	{
		Qv[i] = *(Qpointer+i);
		//printf("%f ", Qv[i]);  /* print first double */
	}


	int j=0;	
	for (int i=numberofmodesV;i< (numberofmodesL + numberofmodesV) ;i++)
	{
		Ql[j] = *(Qpointer+i);
		//printf("%f ", Ql[j]);  /* print first double */
		j++;
	}

	//printf("\n");
}

int AddF(int c, double *fpointer)
{

	double *Fv = (double*)circuits[c].vpparams[2];
	double *Fl = (double*)circuits[c].vpparams[14];

	double *Wv = (double*)circuits[c].vpparams[4];
	double *Wl = (double*)circuits[c].vpparams[16];	

	int numberofmodesV = circuits[c].iparams[0];
	int numberofmodesL = circuits[c].iparams[1];




	for (int i=0;i<numberofmodesV;i++)
	{
		Fv[i] = *(fpointer+i);
		Wv[i] = (2*PI* (*(fpointer+i) ) );
		//printf("%f ", Fv[i]);  /* print first double */
	}

	int j = 0;
	for (int i=numberofmodesV;i< (numberofmodesL + numberofmodesV) ;i++)
	{
		Fl[j] = *(fpointer+i);
		Wl[j] = (2*PI* (*(fpointer+i) ) );
		//printf("%f ", Fl[j]);  /* print first double */
		j++;
	}

	//printf ("\n");

	
}

int AddM(int c, double *Mpointer)
{
		
	double *Mv = (double*)circuits[c].vpparams[3];
	double *Ml = (double*)circuits[c].vpparams[15];


	int numberofmodesV = circuits[c].iparams[0];
	int numberofmodesL = circuits[c].iparams[1];




	for (int i=0;i<numberofmodesV;i++)
	{
		Mv[i] = *(Mpointer+i);
		//printf("%f ", Mv[i]);  /* print first double */
	}

	int j = 0;
	for (int i=numberofmodesV;i< (numberofmodesL + numberofmodesV) ;i++)
	{
		Ml[j] = *(Mpointer+i);
		//printf("%f ", Ml[j]);  /* print first double */
		j++;
	}
	//printf("\n");
}

int StartingPoint(int c, double *StartingPoint)
{
	circuits[c].params[3] = *(StartingPoint+0); //x
	circuits[c].params[4] = *(StartingPoint+1);	//y
	circuits[c].params[5] = *(StartingPoint+2);	//z
	//printf("%f %f %f \n", circuits[c].params[3], circuits[c].params[4], circuits[c].params[5]);

	double *Xv = (double*)circuits[c].vpparams[9];
	double *Yv = (double*)circuits[c].vpparams[10];
	double *Zv = (double*)circuits[c].vpparams[11];

	double *Xl = (double*)circuits[c].vpparams[21];
	double *Yl = (double*)circuits[c].vpparams[22];
	double *Zl = (double*)circuits[c].vpparams[23];

	int numberofmodesV = circuits[c].iparams[0];
	int numberofmodesL = circuits[c].iparams[1];

	for (int i=0;i<numberofmodesV;i++)
	{
		Xv[i] = circuits[c].params[3];
		Yv[i] = circuits[c].params[4];
		Zv[i] = circuits[c].params[5];

	}

	int j = 0;
	for (int i=numberofmodesV;i< (numberofmodesL + numberofmodesV) ;i++)
	{
		Xl[j] = circuits[c].params[3];
		Yl[j] = circuits[c].params[4];
		Zl[j] = circuits[c].params[5];
		j++;
	}


}


void RunAdvancedCantilever(circuit *c)
{
        double *kv = (double*)c->vpparams[0];
        double *kl = (double*)c->vpparams[12];
        
        double *Qv = (double*)c->vpparams[1];
		double *Ql = (double*)c->vpparams[13];

		double *Fv = (double*)c->vpparams[2];
		double *Fl = (double*)c->vpparams[14];

		double *Wv = (double*)c->vpparams[4];
		double *Wl = (double*)c->vpparams[16];	

		double *Mv = (double*)c->vpparams[3];
		double *Ml = (double*)c->vpparams[15];	

		double *Gammav = (double*)c->vpparams[5];
		double *Gammal = (double*)c->vpparams[17];

		double *Vv = (double*)c->vpparams[6];
		double *Vl = (double*)c->vpparams[18];

		double *Xv = (double*)c->vpparams[9];
		double *Yv = (double*)c->vpparams[10];
		double *Zv = (double*)c->vpparams[11];

		double *Xl = (double*)c->vpparams[21];
		double *Yl = (double*)c->vpparams[22];
		double *Zl = (double*)c->vpparams[23];

		double *Av = (double*)c->vpparams[7];
		double *Al = (double*)c->vpparams[19];	

		double *Velocityv = (double*)c->vpparams[8];
		double *Velocityl = (double*)c->vpparams[20];				

		int numberofmodesV = c->iparams[0];
		int numberofmodesL = c->iparams[1];			

		/*
		printf("%f %f %f\n",kv[0],kv[1], kl[0]);
		printf("%f %f %f\n",Qv[0],Qv[1], Ql[0]);
		printf("%f %f %f\n",Fv[0],Fv[1], Fl[0]);
		printf("%f %f %f\n",Wv[0],Wv[1], Wl[0]);
		printf("%f %f %f\n",Mv[0],Mv[1], Ml[0]);
		printf("%f %f %f\n",c->params[3],c->params[4],c->params[5]);
		printf("\n");
		*/




		if (c->iparams[2] == 0) 
		{

				for (int i=0;i<numberofmodesV;i++)
				{
					// on the first run work out the gammas
					Gammav[i] = 0.5 * Wv[i] / Qv[i];
					//printf("%f %f %f\n",Xv[i],Yv[i],Zv[i] );

					if (Mv[i]==0) {
						printf("WARNING: calculating masses from omega and k for vertical eigenfrequency %i\n",i+1 );
						Mv[i]=(Wv[i]*Wv[i] )/kv[i];
						
							  }


				}


				
				int j = 0;
				for (int i=numberofmodesV;i< (numberofmodesL + numberofmodesV) ;i++)
				{
					Gammal[j] = 0.5 * Wl[j] / Ql[j]; 
					//printf("%f %f %f\n",Xl[j],Yl[j],Zl[j] );
					if (Ml[j]==0) {
						printf("WARNING: calculating masses from omega and k for lateral eigenfrequency %i\n",j+1 );
						Ml[j]=(Wl[j]*Wl[j] )/kl[j];
							  }
					j++;
				}

				c->iparams[2] = 1;
		}

		//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		// vertical modes
		//ztip = 0

		double totalforce = GlobalSignals[c->inputs[5]] + GlobalSignals[c->inputs[0]]; 


		for (int i=0; i<numberofmodesV;i++)
		{
			//change in acceleration
			//force / mass                  - z * w ^2 
			Av[i] = totalforce / Mv[i] - Zv[i]*Wv[i]*Wv[i];

			//update the half velocity
			Vv[i] = Vv[i] *(1 - Gammav[i]*dt) + 0.5 * Av[i] * dt;

			// print out V and Z for each mode
			GlobalBuffers[c->outputs[5+i]] = Vv[i];
			GlobalBuffers[c->outputs[6+i+numberofmodesV]] = Zv[i];
			
		}





		c->params[6] = 0;

		for (int i=0; i<numberofmodesV;i++)
		{
			//verlet eqn
			// z + (velocity - friction*velocity) + 0.5 * a * dt^2
			Zv[i] = Zv[i] + Vv[i]*dt*(1 - Gammav[i]*dt ) + 0.5 * Av[i]*dt*dt;
			// half step velocity update
			// v = velocity - velocity*friction	
			Vv[i] = Vv[i] * ( 1 - Gammav[i]*dt) + 0.5*Av[i]*dt;
			c->params[6] = 	c->params[6] + Zv[i];		
		}

		//output ztip
		GlobalBuffers[c->outputs[0]] = c->params[6];
		//
		Velocityv[0] = 0.5 * (c->params[6] - c->params[7])/dt;
		//ztip0 = ztip
		c->params[7]=c->params[6];

		//output absolute pos        =        holder                   +  tip pos
		GlobalBuffers[c->outputs[2]] = GlobalSignals[c->inputs[2]]; 				  //x
		GlobalBuffers[c->outputs[3]] = GlobalSignals[c->inputs[3]] + c->params[8]; //y
		GlobalBuffers[c->outputs[4]] = GlobalSignals[c->inputs[4]] + c->params[6]; //z


/*
		// total force = Force + exciterV
		double totalforce = GlobalSignals[c->inputs[5]] + GlobalSignals[c->inputs[0]]; 


		for (int i=0; i<numberofmodesV;i++)
		{
			//change in acceleration
			//force / mass                  - z * w ^2 
			Av[i] = totalforce / Mv[i] - Zv[i]*Wv[i]*Wv[i];

			//update the half velocity
			Vv[i] = Vv[i] *(1 - Gammav[i]*dt) + 0.5 * Av[i] * dt;

			// print out V and Z for each mode
			GlobalBuffers[c->outputs[5+i]] = Vv[i];
			GlobalBuffers[c->outputs[6+i+numberofmodesV]] = Zv[i];
			
		}

*/		
		//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		// lateral modes
		//ytip = 0

		// total force = Force + exciterY
		totalforce = GlobalSignals[c->inputs[6]] + GlobalSignals[c->inputs[1]]; 


		for (int i=0; i<numberofmodesL;i++)
		{
			//change in acceleration
			//force / mass                  - z * w ^2 
			Al[i] = totalforce / Ml[i] - Yl[i]*Wl[i]*Wl[i];

			//update the half velocity
			Vl[i] = Vl[i] *(1 - Gammal[i]*dt) + 0.5 * Al[i] * dt;

			// print out V and Z for each mode
			GlobalBuffers[c->outputs[7+i+numberofmodesV]] = Vl[i];
			GlobalBuffers[c->outputs[8+i+numberofmodesV+numberofmodesL]] = Yl[i];
			
		}


		
		c->params[8] = 0;

		for (int i=0; i<numberofmodesL;i++)
		{
			//verlet eqn
			// y + (velocity - friction*velocity) + 0.5 * a * dt^2
			Yl[i] = Yl[i] + Vl[i]*dt*(1 - Gammal[i]*dt ) + 0.5 * Al[i]*dt*dt;
			// half step velocity update
			// v = velocity - velocity*friction	
			Vl[i] = Vl[i] * ( 1 - Gammal[i]*dt) + 0.5*Al[i]*dt;
			c->params[8] = 	c->params[8] + Yl[i];		
		}

		//output ytip
		GlobalBuffers[c->outputs[1]] = c->params[8];
		
		Velocityl[0] = 0.5 * (c->params[8] - c->params[9])/dt;
		//ytip0 = ytip
		c->params[9]=c->params[8];

		//output absolute pos        =        Holder               +  tip pos
		GlobalBuffers[c->outputs[2]] = GlobalSignals[c->inputs[2]]; 				  //x
		GlobalBuffers[c->outputs[3]] = GlobalSignals[c->inputs[3]] + c->params[8]; //y
		GlobalBuffers[c->outputs[4]] = GlobalSignals[c->inputs[4]] + c->params[6]; //z


/*
		// total force = Force + exciterY
		totalforce = GlobalSignals[c->inputs[6]] + GlobalSignals[c->inputs[1]]; 


		for (int i=0; i<numberofmodesL;i++)
		{
			//change in acceleration
			//force / mass                  - z * w ^2 
			Al[i] = totalforce / Ml[i] - Yl[i]*Wl[i]*Wl[i];

			//update the half velocity
			Vl[i] = Vl[i] *(1 - Gammal[i]*dt) + 0.5 * Al[i] * dt;

			// print out V and Z for each mode
			GlobalBuffers[c->outputs[7+i+numberofmodesV]] = Vl[i];
			GlobalBuffers[c->outputs[8+i+numberofmodesV+numberofmodesL]] = Yl[i];
			
		}
*/

		//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
}


