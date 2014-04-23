/**********************************************************
Flip-Flop circuits definitions.
*********************************************************/

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef COREFLIPFLOP
#include "core_flipflops.h"
#endif



/***********************************************************************
 * Channels:
 * inputs[0] = D
 * inputs[1] = R
 * inputs[2] = clock
 * outputs[0]= Q
 * outputs[1]= Qbar
 * 
 * Parameters:
 * iparams[0] = state Q of the flipflop
 * iparams[1] = old value of clock
 * 
 * ********************************************************************/
int Add_DRFlipFLop(int owner) {

    circuit c = NewCircuit();
    c.nI = 3;
    c.nO = 3;
    
    c.iplen = 2;
    c.iparams = (int*)calloc(c.iplen,sizeof(int));

    c.updatef = DRFlipFlop;
    
    int index = AddToCircuits(c,owner);
    printf("cCore: added DRFlipFlop circuit\n");
    return index;
    
}

void DRFlipFlop( circuit *c ) {
    
    
    //check for clock front: when the clock changed from low to high
    int clock = ((GlobalSignals[c->inputs[2]] > 0) && !(c->iparams[1] > 0))? 1:0;
    
    //printf("%lf %d %d \n",GlobalSignals[c->inputs[2]],c->iparams[1],clock);
    
    c->iparams[1] = (GlobalSignals[c->inputs[2]] > 0)? 1:0; //store the current clock value
    GlobalBuffers[c->outputs[2]] = clock;   
    
    
    //if reset is high...
    if(GlobalSignals[c->inputs[1]] > 0) {
	
	c->iparams[0] = 0; //store the state
	GlobalBuffers[c->outputs[0]] = 0;	
	GlobalBuffers[c->outputs[1]] = 1;
	return;
    }
    
    if(clock == 0) //if the clock has no front, do nothing!
	return;
    
    //if D is high, switch the state
    if(GlobalSignals[c->inputs[0]] > 0) {
	c->iparams[0] = 1 - c->iparams[0]; // 0->1, 1->0
	
	GlobalBuffers[c->outputs[0]] = c->iparams[0]; //Q
	GlobalBuffers[c->outputs[1]] = 1 - c->iparams[1]; //Qbar
    }  
}




/***********************************************************************
 * Channels:
 * inputs[0] = J
 * inputs[1] = K
 * inputs[2] = clock
 * outputs[0]= Q
 * outputs[1]= Qbar
 * 
 * Parameters:
 * iparams[0] = state Q of the flipflop
 * iparams[1] = Qbar
 * iparams[2] = clock
 * 
 * ********************************************************************/
int Add_JKFlipFLop(int owner) {

    circuit c = NewCircuit();
    c.nI = 3;
    c.nO = 3;
    
    c.iplen = 3;
    c.iparams = (int*)calloc(c.iplen,sizeof(int));

    c.updatef = JKFlipFlop;
    
    int index = AddToCircuits(c,owner);
    printf("cCore: added JKFlipFlop circuit\n");
    return index;
    
}


void JKFlipFlop( circuit *c ) {
    
 
    //check for clock front: when the clock changed from low to high
    int clock = ((GlobalSignals[c->inputs[2]] > 0) && !(c->iparams[2] > 0))? 1:0;
    
    //printf("%lf %d %d \n",GlobalSignals[c->inputs[2]],c->iparams[1],clock);

    c->iparams[2] = (GlobalSignals[c->inputs[2]] > 0)? 1:0; //store the current clock value
    GlobalBuffers[c->outputs[2]] = clock;   


    if(clock == 0) //if the clock has no front, do nothing!
    return;
    

    // if J is low and K is high Q=0 Qbar = 1
    if (GlobalSignals[c->inputs[0]] <=0 && GlobalSignals[c->inputs[1]] >0)
    {
        c->iparams[0] = 0;
        c->iparams[1] = 1;
    }


    // if J is high and K is low Q=1 Qbar = 0
    if (GlobalSignals[c->inputs[0]] >0 && GlobalSignals[c->inputs[1]] <=0)
    {
        c->iparams[0] = 1;
        c->iparams[1] = 0;
    }

    
    // if J is high and K is high Q=Qbar Qbar = Q
    if (GlobalSignals[c->inputs[0]] >0 && GlobalSignals[c->inputs[1]] >0)
    {
        int tempQ = c->iparams[0];      
        c->iparams[0] = c->iparams[1];
        c->iparams[1] = tempQ;

    }
    
    GlobalBuffers[c->outputs[0]] = c->iparams[0]; //Q
    GlobalBuffers[c->outputs[1]] = c->iparams[1]; //Qbar
}



/***********************************************************************
 * Channels:
 * inputs[0] = D
 * inputs[1] = clock
 * outputs[0]= Q
 * outputs[1]= Qbar
 * 
 * Parameters:
 * iparams[0] = state Q of the flipflop
 * iparams[1] = Qbar
 * iparams[2] = Q prev
 * iparams[3] = clock
 * 
 * ********************************************************************/
int Add_DFlipFLop(int owner) {

    circuit c = NewCircuit();
    c.nI = 2;
    c.nO = 3;
    
    c.iplen = 4;
    c.iparams = (int*)calloc(c.iplen,sizeof(int));
    
    c.updatef = DFlipFlop;
    
    int index = AddToCircuits(c,owner);
    printf("cCore: added DFlipFlop circuit\n");
    return index;
}


void DFlipFlop( circuit *c ) {
    
    
    //check for clock front: when the clock changed from low to high
    int clock = ((GlobalSignals[c->inputs[1]] > 0) && !(c->iparams[3] > 0))? 1:0;
    
    //printf("%lf %d %d \n",GlobalSignals[c->inputs[2]],c->iparams[1],clock);
    
    c->iparams[3] = (GlobalSignals[c->inputs[1]] > 0)? 1:0; //store the current clock value
    GlobalBuffers[c->outputs[1]] = clock;   



    if(clock == 0) //if the clock has no front, do nothing!
    return;

    // if D is low and Qprev is low Q=0
    if (GlobalSignals[c->inputs[0]] <= 0 && c->iparams[2] <= 0)
    {
        c->iparams[0] = 0;
        c->iparams[1] = 1;

    }
    
    // if D is low and Qprev is high Q=0
    if (GlobalSignals[c->inputs[0]] <= 0 && c->iparams[2] > 0)
    {

        c->iparams[0] = 0;
        c->iparams[1] = 1;
    }

    // if D is high and Qprev is low Q=1
    if (GlobalSignals[c->inputs[0]] > 0 && c->iparams[2] <= 0)
    {
        c->iparams[0] = 1;
        c->iparams[1] = 0;
    }


    // if D is high and Qprev is high Q=1
    if (GlobalSignals[c->inputs[0]] > 0 && c->iparams[2] > 0)
    {
        c->iparams[0] = 1;
        c->iparams[1] = 0;
    }    

    c->iparams[2] = c->iparams[0];
    GlobalBuffers[c->outputs[0]] = c->iparams[0]; //Q
    GlobalBuffers[c->outputs[1]] = c->iparams[1]; //Qbar
}



/***********************************************************************
 * Channels:
 * inputs[0] = S
 * inputs[1] = R
 * inputs[2] = clock
 * outputs[0]= Q
 * outputs[1]= Qbar
 * 
 * Parameters:
 * iparams[0] = state Q of the flipflop
 * iparams[1] = old value of clock
 * 
 * ********************************************************************/
int Add_SRFlipFLop(int owner) {

    circuit c = NewCircuit();
    c.nI = 3;
    c.nO = 3;
    
    c.iplen = 2;
    c.iparams = (int*)calloc(c.iplen,sizeof(int));

    c.updatef = SRFlipFlop;
    
    int index = AddToCircuits(c,owner);
    printf("cCore: added DRFlipFlop circuit\n");
    return index;
    
}

void SRFlipFlop( circuit *c ) {
    
    
    //check for clock front: when the clock changed from low to high
    int clock = ((GlobalSignals[c->inputs[2]] > 0) && !(c->iparams[1] > 0))? 1:0;
    
    //printf("%lf %d %d \n",GlobalSignals[c->inputs[2]],c->iparams[1],clock);
    
    c->iparams[1] = (GlobalSignals[c->inputs[2]] > 0)? 1:0; //store the current clock value
    GlobalBuffers[c->outputs[2]] = clock;   
    
    
    //if reset is high...
    if(GlobalSignals[c->inputs[1]] > 0) {
    
    c->iparams[0] = 0; //store the state
    GlobalBuffers[c->outputs[0]] = 0;   
    GlobalBuffers[c->outputs[1]] = 1;
    return;
    }
    
    if(clock == 0) //if the clock has no front, do nothing!
    return;
    
    if(GlobalSignals[c->inputs[0]] > 0 && GlobalSignals[c->inputs[1]] <= 0) 
    {
    c->iparams[0] = 1; //store the state
    GlobalBuffers[c->outputs[0]] = 1;   
    GlobalBuffers[c->outputs[1]] = 0;
    }
    
}