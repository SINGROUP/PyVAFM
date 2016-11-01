/**********************************************************
Scanner circuit & its functions
*********************************************************/
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef CORESCANNER
#include "core_scanner.h"
#endif

double* ScannerParams(int index) {
	return circuits[index].params;
}

void Scanner_DoIdle( circuit *c ) {
    //this is the default scanner update function
    //...
    //which does nothing!
}

int Scanner( int owner ) {
	
    circuit c = NewCircuit();
    c.nI = 0;
    c.nO = 4;
    
    c.plen = 13;
    c.params = (double*)calloc(c.plen,sizeof(double));
	
    c.iplen = 6;
    c.iparams = (int*)calloc(c.iplen,sizeof(int));

    c.vplen = 4;
    c.vpparams = (unsigned long long int*)calloc(c.vplen,sizeof(unsigned long long int));    
   
    c.updatef = Scanner_DoIdle; //this is the default scanner update function
    
    int index = AddToCircuits(c,owner);
    printf("cCore: Scanner Initialised\n");
    return index;

}
/****************************************
 * params[0-2] = x,y,z
 * params[3-5] = target x,y,z
 * params[6] = velocity - deprecated
 * params[7-9] = movement step sizes x,y,z
 * params[10] = sin freq
 * params[11] = sin amp
 *
 * 
 * iparams[0] = steps required to complete action (not used)
 * iparams[1] = elapsed steps (not used)
 * iparams[2] = fast scan resolution - points per line
 * iparams[3] = slow scan resolution - lines
 * iparams[4] = number of steps to wait before activating record 
 * iparams[5] = elapsed steps since the last record event 
 *
 * vparams[0] = steps required to complete action Long long int version
 * vparams[1] = elapsed steps Long long int version
 * 
 * *************************************/

unsigned long long int Scanner_Move(int index, double x, double y, double z, double v) {
	
    circuits[index].updatef = Scanner_DoMove;
    //circuit c = circuits[index]; //this is very unsafe!

    // target x
    circuits[index].params[3] = circuits[index].params[0] + x;
    circuits[index].params[4] = circuits[index].params[1] + y;
    circuits[index].params[5] = circuits[index].params[2] + z;
    circuits[index].params[6] = v; //velocity

    // time duration
    double length = x*x + y*y + z*z;
    length = sqrt(length);
    
    double timeneeded = length/v;
    unsigned long long int steps = (unsigned long long int)ceil(timeneeded/dt);
    //printf("%e %e %e \n", steps, (timeneeded/dt), ceil(timeneeded/dt)  );
    //circuits[index].iparams[0] = steps;
    circuits[index].vpparams[0] = (unsigned long long int)steps;
    circuits[index].vpparams[1] = 0;
    

    //saves the initial position before moving
    circuits[index].params[7] = circuits[index].params[0];
    circuits[index].params[8] = circuits[index].params[1];
    circuits[index].params[9] = circuits[index].params[2];
    
    return steps;
}
void Scanner_DoMove( circuit *c ) {
	
	c->vpparams[1]++; //increment the elapsed time



    // pos = pos + step
    c->params[0] = c->params[7] + (unsigned long long int)c->vpparams[1]*(c->params[3]-c->params[7])/ (unsigned long long int)c->vpparams[0];
    c->params[1] = c->params[8] + (unsigned long long int)c->vpparams[1]*(c->params[4]-c->params[8])/ (unsigned long long int)c->vpparams[0];
    c->params[2] = c->params[9] + (unsigned long long int)c->vpparams[1]*(c->params[5]-c->params[9])/ (unsigned long long int)c->vpparams[0];
       
    // at the end adjust all the values to the target
    if ((unsigned long long int)c->vpparams[0] == (unsigned long long int)c->vpparams[1]) {
		
		c->params[0] = c->params[3];
		c->params[1] = c->params[4];
		c->params[2] = c->params[5];
        
		c->updatef = Scanner_DoIdle; //set idle mode
	}
    
    //OUTPUT VALUES
    GlobalBuffers[c->outputs[0]] = c->params[0];
    GlobalBuffers[c->outputs[1]] = c->params[1];
    GlobalBuffers[c->outputs[2]] = c->params[2];
    

    //printf("%f %i %i \n",c->params[0],c->iparams[0],c->iparams[1]);


}

unsigned long long int Scanner_Move_Record(int index, double x, double y, double z, double v, int npts) {
	
	//setup a normal move command
    unsigned long long int steps = Scanner_Move(index,x,y,z,v);
    
    //... but use a different update function
    circuits[index].updatef = Scanner_DoMove_RecordF; //TODO: different for Backward scan!
    
    //nuber of steps to wait between record events
     unsigned long long int dL = ( unsigned long long int)(floor((float)steps/(float)npts));
    circuits[index].vpparams[2] = dL;
    circuits[index].vpparams[3] = 0;
    
    //record the first point
    GlobalBuffers[circuits[index].outputs[3]] = 1;
    
    //return the number of steps to wait for
    return steps;
}

void Scanner_DoMove_RecordF( circuit *c ) {
	
	c->vpparams[3]++; //increment the elapsed time between record events
	
	Scanner_DoMove(c); //do move normally
	
	//if we reached the point where we should record...
	if((unsigned long long int)c->vpparams[3] == (unsigned long long int)c->vpparams[2] || (unsigned long long int)c->vpparams[1] == 1) {
		printf(".");
		GlobalBuffers[c->outputs[3]] = 1;
		c->vpparams[3]=0;
	} else {
		GlobalBuffers[c->outputs[3]] = 0;
	}
	if ((unsigned long long int)c->vpparams[0] == (unsigned long long int)c->vpparams[1]) {
		GlobalBuffers[c->outputs[3]] = 0;
		printf("\n");
	}
	
}


int Scanner_Place (int index, double x,double y, double z) {
    circuits[index].updatef = Scanner_DoPlace;
    circuit c = circuits[index];
    
    // target x
    c.params[0] = x;
    c.params[1] = y;
    c.params[2] = z;

    return 0;
}
void Scanner_DoPlace( circuit *c ) {
    GlobalBuffers[c->outputs[0]] = c->params[0];
    GlobalBuffers[c->outputs[1]] = c->params[1];
    GlobalBuffers[c->outputs[2]] = c->params[2];
   // printf("%f %f %f \n",c->params[0],c->params[1],c->params[2]);

}

unsigned long long int Scanner_MoveTo (int index, double x,double y, double z, double v) {
    
	//circuits[index].updatef = Scanner_DoMoveTo;
	
	//calculate the change
	double dx = x-circuits[index].params[0];
	double dy = y-circuits[index].params[1];
	double dz = z-circuits[index].params[2];

	unsigned long long int steps = Scanner_Move(index, dx, dy, dz, v);

	return steps;
}

void Scanner_DoMoveTo( circuit *c ) { //not needed any more
    // pos = pos + step*direction
    c->params[0] = c->params[0] + c->params[6]*dt*c->params[7];
    c->params[1] = c->params[1] + c->params[6]*dt*c->params[8];
    c->params[2] = c->params[2] + c->params[6]*dt*c->params[9];

    // if increasing then use these 3 if statements
    if (c->params[7]==1){
    if ((c->params[0]) >= (c->params[3]) ) {c->params[0] = c->params[3];}
    }

    if (c->params[8]==1){
    if ((c->params[1]) >= (c->params[4]) ) {c->params[1] = c->params[4];}
    }


    if (c->params[9]==1){
    if ((c->params[2]) >= (c->params[5]) ) {c->params[2] = c->params[5];}
    }


    // if decreasing use these if statements
    if (c->params[7]==-1){
    if ((c->params[0]) <= (c->params[3]) ) {c->params[0] = c->params[3];}
    }

    if (c->params[8]==-1){
    if ((c->params[1]) <= (c->params[4]) ) {c->params[1] = c->params[4];}
    }


    if (c->params[9]==-1){
    if ((c->params[2]) <= (c->params[5]) ) {c->params[2] = c->params[5];}
    }






    (unsigned long long int)c->vpparams[1] ++;
    // at the end adjust all the values
    if ((unsigned long long int)c->vpparams[0] == (unsigned long long int)c->vpparams[1])
        {
            c->params[0] = c->params[3];
            c->params[1] = c->params[4];
            c->params[2] = c->params[5];
        }
    // idle for the time left
    if ((unsigned long long int)c->vpparams[0] == (unsigned long long int)c->vpparams[1]) {c->updatef = Scanner_DoIdle;}
    
    //OUTPUT VALUES
    GlobalBuffers[c->outputs[0]] = c->params[0];
    GlobalBuffers[c->outputs[1]] = c->params[1];
    GlobalBuffers[c->outputs[2]] = c->params[2];
    

    //printf("%f %f %f \n",c->params[0],c->params[1],c->params[2]);


}



int Scanner_Scan (int index, double x,double y, double z, double v, int points) {
	
    circuits[index].updatef = Scanner_DoScan;
    circuit c = circuits[index];
    
    double changex = x-c.params[0];
    double changey = y-c.params[1];
    double changez = z-c.params[2];

    // target x
    c.params[3] = x;
    c.params[4] = y;
    c.params[5] = z;

    c.params[6] = v;

    // direction
    c.params[7] = 1;
    c.params[8] = 1;
    c.params[9] = 1;
    // check if -ve direction
    if (c.params[0] > c.params[3]){c.params[7] = -1;}
    if (c.params[1] > c.params[4]){c.params[8] = -1;}
    if (c.params[2] > c.params[5]){c.params[9] = -1;}



    // find largest step size
    double stepx = abs(floor( (changex)/ (dt*v) ));
    double stepy = abs(floor( (changey)/ (dt*v) ));
    double stepz = abs(floor( (changez)/ (dt*v) ));

    double steps = stepx;
    if (stepy > steps) {steps = stepy;}
    if (stepz > steps) {steps = stepz;}

    c.iparams[0]=steps;
    c.iparams[1]=0;
    c.iparams[2] = points;
    return steps;
}


void Scanner_DoScan( circuit *c )
{
    int Record = 0;
    // pos = pos + step*direction
    c->params[0] = c->params[0] + c->params[6]*dt*c->params[7];
    c->params[1] = c->params[1] + c->params[6]*dt*c->params[8];
    c->params[2] = c->params[2] + c->params[6]*dt*c->params[9];

    // if increasing then use these 3 if statements
    if (c->params[7]==1){
    if ((c->params[0]) >= (c->params[3]) ) {c->params[0] = c->params[3];}
    }

    if (c->params[8]==1){
    if ((c->params[1]) >= (c->params[4]) ) {c->params[1] = c->params[4];}
    }


    if (c->params[9]==1){
    if ((c->params[2]) >= (c->params[5]) ) {c->params[2] = c->params[5];}
    }


    // if decreasing use these if statements
    if (c->params[7]==-1){
    if ((c->params[0]) <= (c->params[3]) ) {c->params[0] = c->params[3];}
    }

    if (c->params[8]==-1){
    if ((c->params[1]) <= (c->params[4]) ) {c->params[1] = c->params[4];}
    }


    if (c->params[9]==-1){
    if ((c->params[2]) <= (c->params[5]) ) {c->params[2] = c->params[5];}
    }


    c->iparams[1] = c->iparams[1] + 1;
    // at the end adjust all the values
    if ((unsigned long long int)c->vpparams[0] == c->iparams[1])
        {
            c->params[0] = c->params[3];
            c->params[1] = c->params[4];
            c->params[2] = c->params[5];
        }
    // idle for the time left
    if ((unsigned long long int)c->vpparams[0] == c->iparams[1]) {c->updatef = Scanner_DoIdle;}
    if ( (c->iparams[1]%c->iparams[2]) == 0) {Record = 1;}
    
    //OUTPUT VALUES
    GlobalBuffers[c->outputs[0]] = c->params[0];
    GlobalBuffers[c->outputs[1]] = c->params[1];
    GlobalBuffers[c->outputs[2]] = c->params[2];
    GlobalBuffers[c->outputs[3]] = Record;
    
}


unsigned long long int SinScan(int index, double freq, double amp, int cycles)
{   
    circuits[index].updatef = DoSinScan;
    circuit c = circuits[index];

    //save initial pos
    circuits[index].params[7] = circuits[index].params[0];
    circuits[index].params[8] = circuits[index].params[1];
    circuits[index].params[9] = circuits[index].params[2];


    circuits[index].params[10] = freq;
    circuits[index].params[11] = amp;



    
    return (int) ( cycles * (1/freq)/dt );
    
}

void DoSinScan(circuit *c)
{
   c->iparams[1] ++;
   
    GlobalBuffers[c->outputs[2]] = c->params[9] +  cos(2*M_PI*c->iparams[1]*dt*c->params[10])*c->params[11];
}



/*
    c.params[0] = Lvxx; X comp of the x lattice vector
    c.params[1] = Lvxy; Y comp of the x lattice vector
    c.params[2] = Lvxz; Z comp of the x lattice vector

    
    c.params[3] = Lvyx; X comp of the y lattice vector
    c.params[4] = Lvyy; Y comp of the y lattice vector
    c.params[5] = Lvyz; Z comp of the y lattice vector

    c.params[6] = Lvzx; X comp of the z lattice vector
    c.params[7] = Lvzy; Y comp of the z lattice vector
    c.params[8] = Lvzz; Z comp of the z lattice vector

    c.params[9]  = sqrt(Lvxx*Lvxx + Lvxy*Lvxy + Lvxz*Lvxz); mag of x vector
    c.params[10] = sqrt(Lvyx*Lvyx + Lvyy*Lvyy + Lvyz*Lvyz); mag of y vector    
    c.params[11] = sqrt(Lvzx*Lvzx + Lvzy*Lvzy + Lvzz*Lvzz); mag of z vector
*/

int CoordTransform(int owner, double Lvxx,double Lvxy,double Lvxz,   double Lvyx,double Lvyy,double Lvyz,   double Lvzx,double Lvzy,double Lvzz)
{

    circuit c = NewCircuit();
    c.nI = 3;
    c.nO = 3;
    
    c.plen = 12;
    c.params = (double*)calloc(c.plen,sizeof(double));

    c.params[0] = Lvxx;
    c.params[1] = Lvxy;
    c.params[2] = Lvxz;

    
    c.params[3] = Lvyx;
    c.params[4] = Lvyy;
    c.params[5] = Lvyz;

    c.params[6] = Lvzx;
    c.params[7] = Lvzy;
    c.params[8] = Lvzz;

    c.params[9]  = sqrt(Lvxx*Lvxx + Lvxy*Lvxy + Lvxz*Lvxz);
    c.params[10] = sqrt(Lvyx*Lvyx + Lvyy*Lvyy + Lvyz*Lvyz);
    c.params[11] = sqrt(Lvzx*Lvzx + Lvzy*Lvzy + Lvzz*Lvzz);

    
   
    c.updatef = RunCoordTrans; //this is the default scanner update function
    
    int index = AddToCircuits(c,owner);
    printf("cCore: Coordinate Transfomration Initialised\n");
    return index;

}

void RunCoordTrans( circuit *c ) 
{
    double x = GlobalSignals[c->inputs[0]];
    double y = GlobalSignals[c->inputs[1]];  
    double z = GlobalSignals[c->inputs[2]]; 


    double ax = c->params[0];
    double ay = c->params[1];
    double az = c->params[2];

    double bx = c->params[3];
    double by = c->params[4];
    double bz = c->params[5];

    double cx = c->params[6];
    double cy = c->params[7];
    double cz = c->params[8];


    //Find C1
    double posx = (bz*cy*x - by*cz*x - bz*cx*y + bx*cz*y + by*cx*z - bx*cy*z)/ (az*by*cx - ay*bz*cx - az*bx*cy + ax*bz*cy + ay*bx*cz - ax*by*cz);
    //Find C2
    double posy = (az*cy*x - ay*cz*x - az*cx*y + ax*cz*y + ay*cx*z - ax*cy*z)/ (-(az*by*cx) + ay*bz*cx + az*bx*cy - ax*bz*cy - ay*bx*cz + ax*by*cz);
    //Find C3
    double posz = (az*by*x - ay*bz*x - az*bx*y + ax*bz*y + ay*bx*z - ax*by*z)/ (az*by*cx - ay*bz*cx - az*bx*cy + ax*bz*cy + ay*bx*cz - ax*by*cz);



    GlobalBuffers[c->outputs[0]]  = posx*c->params[9];
    GlobalBuffers[c->outputs[1]]  = posy*c->params[10];
    GlobalBuffers[c->outputs[2]]  = posz*c->params[11];


}