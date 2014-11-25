
#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef coreDIPOLE
#include "core_Dipole.h"
#endif

#include <math.h>

/***********************************************************************
    c.params[0]=stepz;
    c.params[1]=oldV;
    c.params[2]=oldForce;

    c.params[3-5] = checks
    
 * ********************************************************************/
int Add_Dipole(int owner, double stepz) {

    circuit c = NewCircuit();
    c.nI = 1;
    c.nO = 1;
    
    c.plen = 6;
    c.params = (double*)calloc(c.plen,sizeof(double));
    c.params[0]=stepz;
    c.params[1]=0;
    c.params[2]=0;
    c.params[3]=0;
    c.params[4]=0;
    c.params[5]=0;

    c.updatef = Dipole;
 
    int index = AddToCircuits(c,owner);
    printf("cCore: added Dipole\n");
    return index;
}

void Dipole( circuit *c ) {

    //printf("%f\n",   GlobalSignals[c->inputs[0]] );
    double Force;
    if (c->params[3] == 0) 
        {
            //for the first step set the value of Vold for the next step
            c->params[1] = GlobalSignals[c->inputs[0]]  ;
            
        }


    if (c->params[3] == 1)
    {
    //from the 2nd step onwards calculate the first derivative
    //first derivative V - vo / dz
    Force = (GlobalSignals[c->inputs[0]] - c->params[1] ) / c->params[0];
    printf("F=%e V=%e Vo=%e\n", Force, GlobalSignals[c->inputs[0]],c->params[1]);
    c->params[1]=GlobalSignals[c->inputs[0]];
    GlobalBuffers[c->outputs[0]] = Force;
     
   
    }


    if (c->params[4] == 0 && c->params[3] == 1)
    {
        //For only the second step find Old force but make sure this if statement is not executed on the first rust (thats hwy there is params 3 term)
        //printf("%f\n",Force );
        c->params[2] = Force;
        c->params[4] = 1;  
    }



    if (c->params[5] == 1)
    {
    //From step 3 onwards calculate 2nd derivative
    //2nd derivative F-Fo / dz
    GlobalBuffers[c->outputs[0]] = (Force - c->params[2])/c->params[0];
    printf("Out=%e F=%e Fo=%f \n", GlobalBuffers[c->outputs[0]], Force, c->params[2]);
    
    c->params[2]=Force;
    
    
    }
    
if( c->params[3] ==1 ){ c->params[5] = 1; }




c->params[3] = 1;  


      
         
}


