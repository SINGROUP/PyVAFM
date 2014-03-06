/**********************************************************
Filters circuits definitions.
 *********************************************************/
#include <math.h>

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef COREFILTERS
#include "core_filters.h"
#endif


/*********************************************************
 * Sallen-Key lowpass filter.
 * params[0] fcut
 * params[1] Q
 * params[2] gain
 * params[3] wc
 * params[4] gamma
 * params[5] alpha
 * params[6] yo
 * params[7] yoo
 * ******************************************************/
int Add_SKLP(int owner, double fcut, double Q, double gain) {
	
	circuit c = NewCircuit();
	c.nI = 1;
	c.nO = 1;
	
	c.plen = 8;
	c.params = (double*)calloc(c.plen,sizeof(double));
	
	double wc = fcut * 2 * PI * dt;
	double gamma = wc / (2*Q);
	wc = wc * wc;
	double alpha = 1.0/(1.0+gamma+wc);
	
	c.params[0] = fcut;
	c.params[1] = Q;
	c.params[2] = gain;
	c.params[3] = wc;
	c.params[4] = gamma;
	c.params[5] = alpha;
	c.params[6] = 0;
	c.params[7] = 0;
	
	c.updatef = SKLP;
	
	int index = AddToCircuits(c,owner);
	printf("cCore: added SKLP filter\n");
	return index;
}

void SKLP( circuit *c ) {
	
	double v = GlobalSignals[c->inputs[0]];
	//printf("filtered1\n");
	v = c->params[2]*c->params[3]*v + (2.0*c->params[6]-c->params[7]) + c->params[4]*c->params[7];
	v = v * c->params[5];
	GlobalBuffers[c->outputs[0]] = v;

	c->params[7] = c->params[6];
	c->params[6] = v;
	
}


/*********************************************************
* Sallen-Key Highpass filter.
* params[0] fcut
* params[1] Q
* params[2] gain
* params[3] wc
* params[4] gamma
* params[5] alpha
* params[6] yo
* params[7] yoo
* params[8] xo
* params[9] xoo
* ******************************************************/
int Add_SKHP(int owner, double fcut, double Q, double gain) {
        
        circuit c = NewCircuit();
        c.nI = 1;
        c.nO = 1;
        
        c.plen = 10;
        c.params = (double*)calloc(c.plen,sizeof(double));
        
        double wc = fcut * 2 * PI * dt;
        double gamma = wc / (2*Q);
        wc = wc * wc;
        double alpha = 1.0/(1.0+gamma+wc);

        
        c.params[0] = fcut; 
        c.params[1] = Q; 
        c.params[2] = gain;
        c.params[3] = wc; 
        c.params[4] = gamma;
        c.params[5] = alpha;
        //yo
        c.params[6] = 0;
        //yoo
        c.params[7] = 0;
        
        //xo
        c.params[8] = 0;
        //xoo
        c.params[9] = 0;
        
        c.updatef = SKHP;
        
        int index = AddToCircuits(c,owner);
        printf("added SKHP filter\n");
        return index;
}

void SKHP( circuit *c ) {
        
        double v = GlobalSignals[c->inputs[0]];
        //printf("filtered1\n");
        v = (2*c->params[6]-c->params[7]) + c->params[4]*c->params[7] + c->params[2]*(c->params[9]-2.0*c->params[8]+v);
        v = v * c->params[5];
        GlobalBuffers[c->outputs[0]] = v;


        //yoo and yo (previous inputs)
        c->params[7] = c->params[6];
        c->params[6] = v;

        //xoo and xo (previous outputs)
        c->params[9] = c->params[8];
        c->params[8] = GlobalSignals[c->inputs[0]];
        


        
}


/*********************************************************
* sallen key Band pass filter.
* params[0] fcut
* params[1] band
* params[2] gain
* params[3] wc
* params[4] gamma
* params[5] alpha
* params[6] yo
* params[7] yoo
* params[8] xo
* params[9] xoo
* ******************************************************/
int Add_SKBP(int owner, double fcut, double band, double gain) {
    
    circuit c = NewCircuit();
    c.nI = 1;
    c.nO = 1;
    
    c.plen = 10;
    c.params = (double*)calloc(c.plen,sizeof(double));
    
    double gamma = fcut/band;
    double wc = 2 * PI * fcut * dt;
    gamma = wc/(2*gamma);
    double alpha = 1.0/(1.0 + gamma + wc*wc);
    
    c.params[0] = fcut; 
    c.params[1] = band; 
    c.params[2] = gain; 
    c.params[3] = wc; 
    c.params[4] = gamma;
    c.params[5] = alpha;
    //yo
    c.params[6] = 0;
    //yoo
    c.params[7] = 0;
    //xo
    c.params[8] = 0;
    //xoo
    c.params[9] = 0;
    //c.params[10] = band; 
		    
    c.updatef = SKBP;
    
    
    int index = AddToCircuits(c,owner);
    printf("cCore: added SKBP filter\n");
    return index;
}

void SKBP( circuit *c ) {
        
    double v = GlobalSignals[c->inputs[0]];
   
    v = c->params[2]*c->params[4]*(v-c->params[9]) + c->params[4]*c->params[7] + 
	(2.0*c->params[6]-c->params[7]);
    v = v * c->params[5];
    GlobalBuffers[c->outputs[0]] = v;
    //printf("filtered1 %lf \n",v);

    //yoo and yo (previous inputs)
    c->params[7] = c->params[6];
    c->params[6] = v;

    //xoo and xo (previous outputs)
    c->params[9] = c->params[8];
    c->params[8] = GlobalSignals[c->inputs[0]];
	
}



/*********************************************************
* passive low pass filter.
* TODO: ADD DESCRIPTION OF PARAMS/IPARAMS!
* ******************************************************/
int Add_RCLP(int owner, double fcut, int order) {
	
    circuit c = NewCircuit();
    c.nI = 1;
    c.nO = 1;
    
    c.plen = 6 + order*3;
    c.params = (double*)calloc(c.plen,sizeof(double));

    c.iplen=1;
    c.iparams = (int*)calloc(c.plen,sizeof(double));
    
    fcut = 2*PI*fcut;
    double a = 2*dt*fcut;
    a = a/(1+a);
    
    
    c.params[0] = fcut;
    c.params[1] = a;
    
    c.iparams[0] = order;

    for (int i=2; i<=(5+order*3); i++){
	    c.params[i] = 0;
    }

    //[0]=fcut
    //[1]=a
    //[2 to order+2] = y
    //[order+3 to order*2+3] = yo
    //[order*2+4 to order*3+4] = yoo


    c.updatef = RCLP;
    int index = AddToCircuits(c,owner);
    return index;
}

void RCLP( circuit *c ) {
        
        int order = c->iparams[0];

        int trackery = 2;
        int trackeryo = order +3;
        int trackeryoo = order*2 +4;

        c->params[trackery] = GlobalSignals[c->inputs[0]];

        for (int i=0; i<order;i++)
            {
            //y[i+1]              = a           * y[i]              +  (1-a)              *  y00[i+1] 
            c->params[trackery+i+1] = c->params[1]*c->params[trackery+i] + (1- c->params[1] ) *  c->params[trackeryoo+i+1];
            }
        

        GlobalBuffers[c->outputs[0]]  = c->params[trackery+order];

        for (int i=0; i<order+1;i++)
            {
             //y00 = y0
            c->params[trackeryoo+i]  = c->params[trackeryo+i];
             // y0=y
            c->params[trackeryo+i]   = c->params[trackery+i];
            }    
}

/*********************************************************
* passive low pass filter.
* TODO: ADD DESCRIPTION OF PARAMS/IPARAMS!
* ******************************************************/
int Add_RCHP(int owner, double fcut, int order) {
    
    circuit c = NewCircuit();
    c.nI = 1;
    c.nO = 1;
    
    c.plen = 6 + order*3;
    c.params = (double*)calloc(c.plen,sizeof(double));

    c.iplen=1;
    c.iparams = (int*)calloc(c.plen,sizeof(double));
    
    fcut = 2*PI*fcut;
    double a = 2*dt*fcut;
    a = a/(1+a);
    
    
    c.params[0] = fcut;
    c.params[1] = a;
    
    c.iparams[0] = order;

    for (int i=2; i<=(5+order*3); i++){
        c.params[i] = 0;
    }

    //[0]=fcut
    //[1]=a
    //[2 to order+2] = y
    //[order+3 to order*2+3] = yo
    //[order*2+4 to order*3+4] = yoo


    c.updatef = RCHP;
    int index = AddToCircuits(c,owner);
    return index;
}

void RCHP( circuit *c ) {
        
        int order = c->iparams[0];

        int trackery = 2;
        int trackeryo = order +3;
        int trackeryoo = order*2 +4;

        c->params[trackery] = GlobalSignals[c->inputs[0]];

        for (int i=0; i<order;i++)
            {
            //y[i+1]                = (y[i]                  -  yoo[i]                  +  yoo[i+1]                 )*a 
            c->params[trackery+i+1] = (c->params[trackery+i] -  c->params[trackeryoo+i] +  c->params[trackeryoo+i+1])*c->params[1];
            }
        

        GlobalBuffers[c->outputs[0]]  = c->params[trackery+order];

        for (int i=0; i<order+1;i++)
            {
             //y00 = y0
            c->params[trackeryoo+i]  = c->params[trackeryo+i];
             // y0=y
            c->params[trackeryo+i]   = c->params[trackery+i];
            }    
}

