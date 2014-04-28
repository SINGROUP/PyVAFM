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
int Add_VDW(int owner, double gamma, double hamaker, double radius, double offset) {

    circuit c = NewCircuit();
    c.nI = 1;
    c.nO = 1;
    
    double TipAngle = gamma;
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
    //TipHamak = TipHamak* 1.0e18;//converted in NANONEWTON-NANOMETER

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
    printf("cCore: added VDW circuit\n");
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















/***********************************************************************
    c.params[0] = tipoffset; 
    c.params[1] = A1;
    c.params[2] = A2;
    c.params[3] = A3;
    c.params[4] = A4;
    c.params[5] = A5;
 * ********************************************************************/
int Add_VDWtorn(int owner, double A1, double A2, double A3, double A4, double A5, double A6 ,double tipoffset ) {

    circuit c = NewCircuit();
    c.nI = 1;
    c.nO = 1;

    c.plen = 7;
    c.params = (double*)calloc(c.plen,sizeof(double));

    c.params[0] = tipoffset; 
    c.params[1] = A1;
    c.params[2] = A2;
    c.params[3] = A3;
    c.params[4] = A4;
    c.params[5] = A5;
    c.params[6] = A6;

    c.updatef = VDWtorn;    

    int index = AddToCircuits(c,owner);
    printf("cCore: added VDWtorn circuit\n");
    return index;
    
}


void VDWtorn( circuit *c ) {

    double ztip = GlobalSignals[c->inputs[0]] + c->params[0];

    if (ztip == 0)
    {
        return;
    }

    //double vdw = A1 * A2 * exp (-A2 * x) + (10* A5 / x^11) + (8* A4 / x^9) + (6* A5 / x^7)+ (4* A6 / x^5); 
    double vdw = c->params[1] * c->params[2] * exp(-c->params[2] * ztip) + (10* c->params[5] / pow(ztip,11) ) + (8* c->params[4] / pow(ztip,9) ) + (6* c->params[3] / pow(ztip,7) ) + (4* c->params[6] / pow(ztip,5) ); 
    //vdw = vdw * -1;

    //printf("%e %e \n", ztip,vdw);
    GlobalBuffers[c->outputs[0]] = vdw;    

}