/**********************************************************
Comparison circuits definitions.
*********************************************************/

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef CORESIGNALPROCESSING
#include "core_signalprocessing.h"
#endif



int Add_gain(int owner, double gainvalue) {

        circuit c = NewCircuit();
        c.nI = 1;
        c.nO = 1;
        
        c.plen = 1;
        c.params = (double*)calloc(c.plen,sizeof(double));
        
        c.params[0] = gainvalue;
        
        c.updatef = gain;
        
        int index = AddToCircuits(c, owner);
        printf("cCore: added Gain circuit\n");
        return index;
}
void gain( circuit *c ) {

    GlobalBuffers[c->outputs[0]] = GlobalBuffers[c->inputs[0]]* c->params[0];
}


int Add_minmax(int owner, double checktime) {

    circuit c = NewCircuit();
    c.nI = 1;
    c.nO = 4;
    
    c.plen = 2;
    c.params = (double*)calloc(c.plen,sizeof(double));
    
    
    c.iplen = 2;
    c.iparams = (int*)calloc(c.iplen,sizeof(int));
    
    c.iparams[0] = (int)(floor(checktime/dt)); //checktime in steps
    c.iparams[1] = 0; //step counter
    
    c.updatef = minmax;
    
    int index = AddToCircuits(c, owner);
    printf("added minmax circuit %i\n",c.iparams[0]);
    return index;
}
void minmax( circuit *c ) {

    double signal = GlobalSignals[c->inputs[0]];
    
    if (signal > c->params[0])
        c->params[0] = signal; //max
    if (signal < c->params[1])
        c->params[1] = signal; //min
    
    c->iparams[1]++;
	
	//if the counter is equal to the amount of time steps then then output the values
    if (c->iparams[1] >= c->iparams[0]) {

        GlobalBuffers[c->outputs[0]] = c->params[0];
        GlobalBuffers[c->outputs[1]] = c->params[1];

        GlobalBuffers[c->outputs[2]] = (c->params[0] - c->params[1])*0.5;
        GlobalBuffers[c->outputs[3]] = (c->params[0] + c->params[1])*0.5;

        //reset min and max for the next calculation
        c->params[1] = signal;
        c->params[0] = signal;

        c->iparams[1] = 0;
    }
    
}


int Add_derivative(int owner) {

    circuit c = NewCircuit();
    c.nI = 1;
    c.nO = 1;
    
    c.plen = 2;
    c.params = (double*)calloc(c.plen,sizeof(double));
    //[0] is yo, [1] is yoo
    
    c.updatef = derivative;
    
    int index = AddToCircuits(c, owner);
    printf("cCore: added derivative circuit\n");
    return index;
}
void derivative(circuit *c) {
    
    double result = 0.5*(GlobalSignals[c->inputs[0]] - c->params[1]) / dt;

    GlobalBuffers[c->outputs[0]] = result;
    
    c->params[1] = c->params[0]; //yoo <- yo
    c->params[0] = GlobalSignals[c->inputs[0]]; //yo <- input
    
}


int Add_integral(int owner) {

    circuit c = NewCircuit();
    c.nI = 1;
    c.nO = 1;
    
    c.plen = 2;
    c.params = (double*)calloc(c.plen,sizeof(double));
    //[0] is the accumulated value
    //[1] is yo
    
    c.updatef = integral;
    
    int index = AddToCircuits(c, owner);
    printf("cCore: added integral circuit\n");
    return index;
}
void integral(circuit *c) {
    
    c->params[0] += (c->params[1] + GlobalSignals[c->inputs[0]])*dt*0.5;
    GlobalBuffers[c->outputs[0]] = c->params[0];

    c->params[1] = GlobalSignals[c->inputs[0]];
    
}


int Add_delay(int owner, int nsteps) {

    circuit c = NewCircuit();
    c.nI = 1;
    c.nO = 1;
    
    c.iplen = 2;
    c.iparams = (int*)calloc(c.iplen, sizeof(int));
    c.iparams[0] = nsteps; //number of steps
    c.iparams[1] = 0; //counter
    
    c.plen = nsteps;
    c.params = (double*)calloc(c.plen,sizeof(double));
    //[0-nsteps-1] buffered value
    
    c.updatef = delay;
    
    int index = AddToCircuits(c, owner);
    printf("cCore: added delay circuit\n");
    return index;
}
void delay(circuit *c) {
    
    GlobalBuffers[c->outputs[0]] = c->params[c->iparams[1]];
    c->params[c->iparams[1]] = GlobalSignals[c->inputs[0]];
    
    c->iparams[1]++;
    if(c->iparams[1] >= c->iparams[0]) {
        c->iparams[1] = 0;
    }
}


int Add_peaker(int owner, int up) {

    circuit c = NewCircuit();
    c.nI = 1;
    c.nO = 3;
    
    c.iplen = 3;
    c.iparams = (int*)calloc(c.iplen, sizeof(int));
    c.iparams[0] = up; //up
    c.iparams[1] = 0; //counter
    c.iparams[2] = 0; //tick
    
    c.plen = 5;
    c.params = (double*)calloc(c.plen,sizeof(double));
    c.params[0] = 0; //y
    c.params[1] = 0; //yo
    c.params[2] = 0; //yoo
    c.params[3] = 0; //delay
    c.params[4] = 0; //peak
    //[0-nsteps-1] buffered value
    
    c.updatef = peaker;
    
    int index = AddToCircuits(c, owner);
    printf("cCore: added peak detector circuit\n");
    return index;
}
void peaker(circuit *c) {
    
        c->params[2] = c->params[1];
        c->params[1] = c->params[0];
        c->params[0] = GlobalSignals[c->inputs[0]];
        c->iparams[2] = 0;

        if(c->params[2] < c->params[1] && c->params[1] > c->params[0] && c->iparams[0]==1) {
            c->iparams[2] = 1;
            c->params[4] = c->params[1];
            c->params[3] = dt*c->iparams[1];
			c->iparams[1] = 0;
        }
        if(c->params[2] > c->params[1] && c->params[1] < c->params[0] && c->iparams[0]!=1) {
            c->iparams[2] = 1;//self.tick = 1  
			c->params[4] = c->params[1];//self.peak= self.yo
            c->params[3] = dt*c->iparams[1];//self.delay = self.counter * self.machine.dt
            c->iparams[1] = 0;//self.counter = 0
        }
        c->iparams[1]++;//self.counter=self.counter + 1

        GlobalBuffers[c->outputs[0]] = c->params[4];//self.O["peak"].value = self.peak
        GlobalBuffers[c->outputs[1]] = (double)(c->iparams[2]);//self.O["tick"].value = self.tick
        GlobalBuffers[c->outputs[2]] = c->params[3];//self.O["delay"].value = self.delay
}


int Add_phasor(int owner) {

    circuit c = NewCircuit();
    c.nI = 2;
    c.nO = 2;
    
    c.iplen = 5;
    c.iparams = (int*)calloc(c.iplen, sizeof(int));
    c.iparams[0] = 0; //counter
    c.iparams[1] = 0; //in1 had wave front
    c.iparams[2] = 0; //in2 had wave front
    c.iparams[3] = 0; //in1 was found
    c.iparams[4] = 0; //in2 was found
    
    c.plen = 2;
    c.params = (double*)calloc(c.plen,sizeof(double));
    c.params[0] = 0; //in1 old
    c.params[1] = 0; //in2 old

    //[0-nsteps-1] buffered value
    
    c.updatef = phasor;
    
    int index = AddToCircuits(c, owner);
    printf("cCore: added phasor circuit\n");
    return index;
}
void phasor(circuit *c) {
    
    int tick = 0;
    
    if(GlobalSignals[c->inputs[0]] > 0 && c->params[0] <= 0)
        c->iparams[1] = 1;
    
    if(GlobalSignals[c->inputs[1]] > 0 && c->params[1] <= 0 && c->iparams[1] == 1)
        c->iparams[2] = 1;

    
    //if we have front1 but not front 2
    if( c->iparams[1] == 1 && c->iparams[2] == 0) {
        c->iparams[0]++; //increment the timer
    }
    
   
    //if we have both fronts
    if( c->iparams[1] == 1 && c->iparams[2] == 1) {
        tick = 1;
        GlobalBuffers[c->outputs[1]] = dt*c->iparams[0];
        c->iparams[1] = 0;
        c->iparams[2] = 0;
        c->iparams[0] = 0;
    }
    
    c->params[0] = GlobalSignals[c->inputs[0]];
    c->params[1] = GlobalSignals[c->inputs[1]];
    
    GlobalBuffers[c->outputs[0]] = tick;

}

int Add_limiter(int owner) {

    circuit c = NewCircuit();
    c.nI = 3;
    c.nO = 1;
    
    
    c.updatef = limiter;
    
    int index = AddToCircuits(c, owner);
    printf("cCore: added limiter circuit\n");
    return index;
}
void limiter(circuit *c) {

    GlobalBuffers[c->outputs[0]] = GlobalSignals[c->inputs[0]];
    if (GlobalSignals[c->inputs[0]] > GlobalSignals[c->inputs[1]]) {
        GlobalBuffers[c->outputs[0]] = GlobalSignals[c->inputs[1]];
    }
    if (GlobalSignals[c->inputs[0]] < GlobalSignals[c->inputs[2]]) {
        GlobalBuffers[c->outputs[0]] = GlobalSignals[c->inputs[2]];
    }
    
}

//iparams[0]: previous value of signal
int Add_flip(int owner) {
    
    circuit c = NewCircuit();
    c.nI = 1;
    c.nO = 1;
    
    c.iplen = 1;
    c.iparams = (int*)calloc(c.iplen,sizeof(int));
    
    c.updatef = flip;
    
    int index = AddToCircuits(c, owner);
    printf("cCore: added flip circuit\n");
    return index;
    
}
void flip(circuit *c) {
    
    int signal = (GlobalSignals[c->inputs[0]] > 0)? 1:0;
        
    GlobalBuffers[c->outputs[0]] = (signal>0 && !(c->iparams[0]>0))? 1:0;
    
    c->iparams[0] = signal;
    
    
}



