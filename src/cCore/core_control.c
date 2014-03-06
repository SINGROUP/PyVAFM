/**********************************************************
Control circuits definitions.
*********************************************************/

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef CORECONTROL
#include "core_control.h"
#endif


/***********************************************************************
 * Channels:
 * inputs[0] = signal
 * inputs[1] = set
 * inputs[2] = Kp
 * inputs[3] = Ki
 * outputs[0]= out
 * 
 * Parameters:
 * params[0] = accumulated integral part
 * params[1] = value of KI*(signal-set) in the previous step
 * 
 * ********************************************************************/
int Add_PI(int owner) {

    circuit c = NewCircuit();
    c.nI = 4;
    c.nO = 1;
    
    c.plen = 2;
    c.params = (double*)calloc(c.plen,sizeof(double));

    c.updatef = PIC;
    
    int index = AddToCircuits(c,owner);
    printf("cCore: added PI circuit\n");
    return index;
    
}

void PIC( circuit *c ) {
    
    double delta = GlobalBuffers[c->inputs[1]] - GlobalBuffers[c->inputs[0]];
    
    double KI = GlobalSignals[c->inputs[3]];
    //double KP = GlobalSignals[c->inputs[2]];
    
    c->params[0] += 0.5*( c->params[1] + KI*delta )*dt;
    GlobalBuffers[c->outputs[0]] = delta*GlobalSignals[c->inputs[2]] + c->params[0];
    c->params[1] = KI*delta;

}

/***********************************************************************
 * Channels:
 * inputs[0] = signal
 * inputs[1] = set
 * inputs[2] = Kp
 * inputs[3] = Ki
 * inputs[4] = Kd
 * outputs[0]= out
 * 
 * Parameters:
 * params[0] = accumulated integral part
 * params[1] = value of KI*(signal-set) in the previous step
 * params[2] = value of delta in the previous step
 * 
 * ********************************************************************/
int Add_PID(int owner) {

    circuit c = NewCircuit();
    c.nI = 5;
    c.nO = 1;
    
    c.plen = 3;
    c.params = (double*)calloc(c.plen,sizeof(double));

    c.updatef = PIDC;
    
    int index = AddToCircuits(c,owner);
    printf("cCore: added PID circuit\n");
    return index;
    
}


void PIDC( circuit *c ) {
    
    double delta = GlobalBuffers[c->inputs[1]] - GlobalBuffers[c->inputs[0]];
    double KI = GlobalSignals[c->inputs[3]];
    //printf("pid time %lf\n",GlobalSignals[0]);
    
    c->params[0] += 0.5*( c->params[1] + KI*delta )*dt;
    
    GlobalBuffers[c->outputs[0]] = delta*GlobalSignals[c->inputs[2]] + 
        c->params[0] + GlobalSignals[c->inputs[4]]*(delta-c->params[2])/dt;

    c->params[1] = KI*delta;
    c->params[2] = delta;

}
