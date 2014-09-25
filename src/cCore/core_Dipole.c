
#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef coreSTM
#include "core_STM.h"
#endif

#include <math.h>

/***********************************************************************
    c.params[0] = Dx;
    c.parmas[1] = Dy;
    c.params[2] = Dz;
    c.params[3] = xo
    c.params[4] = yo
    c.params[5] = zo
    c.params[6] = Vo
    
 * ********************************************************************/
int Add_Dipole(int owner, double Dx, double Dy, double Dz) {

    circuit c = NewCircuit();
    c.nI = 4;
    c.nO = 1;
    
    c.plen = 7;
    c.params = (double*)calloc(c.plen,sizeof(double));
    c.params[0]=Dx;
    c.params[1]=Dy;
    c.params[2]=Dz;
    c.params[3]=0;
    c.params[4]=0;
    c.params[5]=0;
    c.params[6]=0;

    c.updatef = Dipole;
 
    int index = AddToCircuits(c,owner);
    printf("cCore: added Dipole\n");
    return index;
}

void Dipole( circuit *c ) {


    //Figure out dz.
    // d/dz = V(t) - V(t-1)/(z - zo) 
    double dz = GlobalSignals[c->inputs[4]] - c->params[6] / (GlobalSignals[c->inputs[4]] - c->params[5] )

    
    
}


