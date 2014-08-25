/**********************************************************
VDW force circuits definitions.
*********************************************************/

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef coreSTM
#include "core_STM.h"
#endif

#include <math.h>

/***********************************************************************
    c.params[0] = WorkFunction;
    c.parmas[1] = WaveFunction Overlap;
    c.params[2] = Constant;
 * ********************************************************************/
int Add_STM(int owner, double WorkFunction, double WaveFunctionOverlap) {

    circuit c = NewCircuit();
    c.nI = 1;
    c.nO = 1;
    
    c.plen = 3;
    c.params = (double*)calloc(c.plen,sizeof(double));
    c.params[0]=WorkFunction;
    c.params[1]=WaveFunctionOverlap;

    c.updatef = STM;
 
    int index = AddToCircuits(c,owner);
    printf("cCore: added STM\n");
    return index;
}

void STM( circuit *c ) {

    double k = sqrt(2*c->params[0]);
    double S = c->params[1];
 
    double C = 7.82e-4;

    
    double n = GlobalSignals[c->inputs[0]];
    // I = n^2 * k^2 * S^2 * C
    GlobalBuffers[c->outputs[0]] = n*n * k*k * S*S * C;
    
}


