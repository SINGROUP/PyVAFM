/**********************************************************
Flip-Flop circuits definitions.
*********************************************************/

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef coreVDW
#include "core_VDW.h"
#endif

#include <math.h>

/***********************************************************************
    c.params[0] = TipAngle;
    c.parmas[1] = TipHamak;
    c.params[2] = TipRadius;
    c.params[3] = TipOffset;
    c.params[4] = g2r;
    c.params[5] = sing;
    c.parmas[6] = tang;
    c.params[7] = cosg;
    c.params[8] = cos2g;
    c.params[9] = TR2;
    c.params[10] = TRC;
    c.params[11] = TRS;
 * ********************************************************************/
int Add_VDW(int owner, double alpha, double hamaker, double radius, double offset) {

    circuit c = NewCircuit();
    c.nI = 1;
    c.nO = 1;
    
    double TipAngle = alpha;
    double TipHamak = hamaker;
    double TipRadius = radius;
    double TipOffset = offset;
    double g2r = PI/180.0;
    double sing = sin(TipAngle*g2r);
    double tang = tan(TipAngle*g2r);
    double cosg = cos(TipAngle*g2r);
    double cos2g= cos(TipAngle*g2r*2.0);
    double TR2 = TipRadius*TipRadius;
    double TRC = TipRadius*cos2g;
    double TRS = TipRadius*sing;
    TipHamak = TipHamak* 1.0e18;//converted in NANONEWTON-NANOMETER

    c.plen = 12;
    c.params = (double*)calloc(c.plen,sizeof(double));

    c.params[0] = TipAngle;
    c.params[1] = TipHamak;
    c.params[2] = TipRadius;
    c.params[3] = TipOffset;
    c.params[4] = g2r;
    c.params[5] = sing;
    c.params[6] = tang;
    c.params[7] = cosg;
    c.params[8] = cos2g;
    c.params[9] = TR2;
    c.params[10] = TRC;
    c.params[11] = TRS;

    c.updatef = VDW;
    
    int index = AddToCircuits(c,owner);
    printf("cCore: added DRFlipFlop circuit\n");
    return index;
    
}
/***********************************************************************
    c.params[0] = TipAngle;
    c.parmas[1] = TipHamak;
    c.params[2] = TipRadius;
    c.params[3] = TipOffset;
    c.params[4] = g2r;
    c.params[5] = sing;
    c.parmas[6] = tang;
    c.params[7] = cosg;
    c.params[8] = cos2g;
    c.params[9] = TR2;
    c.params[10] = TRC;
    c.params[11] = TRS;
 * ********************************************************************/
void VDW( circuit *c ) {

    // ztip = inputz + offset
    double ztip = GlobalSignals[c->inputs[0]] + c->params[3];

    if (ztip == 0)
    {
        return;
    }


            //vdw = (TipHamak*TR2)*(1.0-sing)*(TRS-ztip*sing-TipRadius-ztip);
            double vdw = (c->params[1]*c->params[9])*(1.0-c->params[5])*(c->params[11]-ztip*c->params[5]-c->params[2]-ztip);

            //vdw/= (6.0*(ztip*ztip)*(TipRadius+ztip-TRS)*(TipRadius+ztip-TRS));
            vdw /= (6.0*(ztip*ztip)*(c->params[2]+ztip-c->params[11])*(c->params[2]+ztip-c->params[11]));

            //vdw-= (TipHamak*tang*(ztip*sing+TRS+TRC))/(6.0*cosg*(TipRadius+ztip-TRS)*(TipRadius+ztip-TRS));
            vdw -= (c->params[1]*c->params[6]*(ztip*c->params[5]+c->params[11]+c->params[10]))/(6.0*c->params[7]*(c->params[2]+ztip-c->params[11])*(c->params[2]+ztip-c->params[11]));

            GlobalBuffers[c->outputs[0]] = vdw;

}