
#include "circuit.h"
#include "core_tutcirc.h"

int Add_TutCirc(int owner, double gain) {

	  circuit c = NewCircuit();
    c.nI = 1;
    c.nO = 1;

    c.plen = 1;
    c.params = (double*)calloc(c.plen,sizeof(double));
    c.params[0]=gain;

    c.updatef = TutCirc;
 
    int index = AddToCircuits(c,owner);
    printf("cCore: added Tutorial Circuit\n");
    return index;

}

void TutCirc( circuit *c ) {
		double input = GlobalSignals[c->inputs[0]];
		GlobalBuffers[c->outputs[0]] = input * c->params[0];

	}


