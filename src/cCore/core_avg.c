/*********************************************************
Averager circuit
*********************************************************/

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef COREAVG
#include "core_avg.h"
#endif


int Add_avg(int owner, int nsteps, int moving) {
	
    circuit c = NewCircuit();

    c.nI = 1;
    c.nO = 1;

	c.iplen = 3;
	c.iparams = (int*)calloc(c.plen,sizeof(double));
	
	c.iparams[0] = nsteps; 
	c.iparams[1] = 0; //counter
	c.iparams[2] = moving; //moving avg
	
	c.plen = nsteps+1;//[nsteps] is the total, [0-nsteps-1] is the buffer
	c.params = (double*)calloc(c.plen,sizeof(double));
    
	c.updatef = avg;
	
	int index = AddToCircuits(c,owner);
	return index;
}


void avg(circuit *c) {
	
		
	int nsteps = c->iparams[0];
	int cnt = c->iparams[1]; //counter
	
	//record the value
	c->params[nsteps] -= c->params[cnt]; //remove the value to overwrite from total
	c->params[cnt] = GlobalSignals[c->inputs[0]]; //record
	
	c->params[nsteps] += c->params[cnt]; //add it to the total
	
	//increment the counter and refit it...
	c->iparams[1]++; 
	if(c->iparams[1] >= nsteps) 
		c->iparams[1] = 0;
	
	if (c->iparams[2] == 1) {
		//output average
		GlobalBuffers[c->outputs[0]] = c->params[nsteps]/nsteps;
	}
	else {
		if(c->iparams[1] == 0)
			GlobalBuffers[c->outputs[0]] = c->params[nsteps]/nsteps;
	}
	
}

