/**********************************************************
Interpolation circuits definitions.
*********************************************************/
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef COREINTER
#include "core_interpolation.h"
#endif

/******************************************************
 * inputs[0-2] 		= coordinates x y z
 * outputs[0-comp-1] 	= interpolated vector field
 * params[0-2] 	= steps dx dy dz
 * params[3-5] 	= sizes of pbc box
 * iparams[0] 	= components
 * iparams[1-3]	= number of points nx ny nz
 * iparams[4] 	= size of field (1 component) nx*ny*nz
 * iparams[5] 	= size of zy plane (1 component) ny*nz
 * iparams[6-8]	= periodic 0|1 along each direction
 * ***************************************************/
int Add_i3Dlin( int owner, int components) {

    //printf("%i \n",xsize);

    circuit c = NewCircuit();
    c.nI = 3;
    c.nO = components;

    c.iplen = 9;
    c.iparams = (int*)calloc(c.iplen,sizeof(int));
    c.iparams[0] = components;


    c.plen = 6;
    c.params = (double*)calloc(c.plen,sizeof(double));
    
    c.vplen = components;
    c.vpparams = (double**)malloc(c.vplen * sizeof(double*));
    for (int i = 0; i < components; i++) {
	c.vpparams[i] = (double*)calloc(1, sizeof(double)); // this is the forcefield
    }
 
    c.updatef = i3Dlin; //this is the default scanner update function
    int index = AddToCircuits(c,owner);
    printf("cCore: i3Dlin initialised\n");
    return index;

}

double** i3Dlin_npts( int c, int nx, int ny, int nz) {
    
    circuits[c].iparams[1] = nx;
    circuits[c].iparams[2] = ny;
    circuits[c].iparams[3] = nz;
    
    circuits[c].iparams[4] = nx*ny*nz;
    circuits[c].iparams[5] = ny*nz;
    
    circuits[c].params[3] = nx*circuits[c].params[0];
    circuits[c].params[4] = ny*circuits[c].params[1];
    circuits[c].params[5] = nz*circuits[c].params[2];
    
    for (int i = 0; i < circuits[c].iparams[0]; i++) {
	circuits[c].vpparams[i] = (double*)realloc(circuits[c].vpparams[i], 
	    nx*ny*nz*sizeof(double));
    }
    
    //double* w = (double*)circuits[c].vpparams[0];
    //w[0] = 123.3;
    
    return circuits[c].vpparams;
}
int i3Dlin_step( int c, double dx, double dy, double dz) {
    
    circuits[c].params[0] = dx;
    circuits[c].params[1] = dy;
    circuits[c].params[2] = dz;
    //printf("cCore: i3Dlin steps: %le %le %le \n",dx,dy,dz);
    circuits[c].params[3] = dx*circuits[c].iparams[1];
    circuits[c].params[4] = dy*circuits[c].iparams[2];
    circuits[c].params[5] = dz*circuits[c].iparams[3];
    
    return 0;
}
int i3Dlin_pbc( int c, int x, int y, int z) {
    
    circuits[c].iparams[6] = x;
    circuits[c].iparams[7] = y;
    circuits[c].iparams[8] = z;
    
    return 0;
}

void i3Dlin( circuit *c ) {
    
    //printf("ASD!\n");
    
    double pos[3];
    int oob = 1;
    




    //position of the tip - pbc
    for (int i = 0; i < 3; i++) {


	pos[i] = GlobalSignals[c->inputs[i]];
	if(c->iparams[i+6] == 1)
	    pos[i] -= floor(pos[i]/c->params[3+i])*c->params[3+i];

	else {
	    if( pos[i] >= (c->iparams[i+1]-1)*c->params[i] || pos[i] < 0) {
		oob = 0;
	    }
	    
	}
    }

    
    if( pos[2] >= (c->iparams[2+1]-1)*c->params[2])
    {

    	oob = 1;
    for (int comp=0; comp<c->iparams[0]; comp++)
	    GlobalBuffers[c->outputs[comp]] = 0;
	return;
    }



    //outputs 0 if out of bounds
    if(oob == 0) {
	printf("WARNING! i3Dlin OOB!\n");
	for (int comp=0; comp<c->iparams[0]; comp++)
	    GlobalBuffers[c->outputs[comp]] = 0;
	return;
    }
    
    //interpolate
    int idx[3], idxx[3];
    double t[3];
    
    //compute voxel indexes and t
    for (int i = 0; i < 3; i++) {
	idx[i] = (int)floor(pos[i]/c->params[i]); //voxel lower indexes
	idxx[i] = idx[i]+1; //voxel higher indexes
	if(idxx[i] == c->iparams[i+1] && c->iparams[i+6]==1)
	    idxx[i] = 0; //wrap to 0 if pbc
	
	//compute t - the position of the tip in the voxel, normalised in 0-1
	t[i] = (pos[i] - idx[i]*c->params[i])/c->params[i];
    }


    if (pos[0] == 15.6) {idxx[0] = 0;}
    if (pos[1] == 13.5) {idxx[1] = 0;}
    if (pos[2] == 14.7) {idxx[2] = 0;}
	
    //printf("asd! %lf %lf %lf\n",pos[0],pos[1],pos[2]);
    //printf("asd! %lf %lf %lf\n",t[0],t[1],t[2]);
    printf("asd! %d %d %d\n",idx[0],idx[1],idx[2]);
    printf("asd! %d %d %d\n",idxx[0],idxx[1],idxx[2]);





    double C000[4];
    double *data;
    int nyz = c->iparams[5], ny = c->iparams[3];
    int indexes[8];
    indexes[0] = idx[0]*nyz + idx[1]*ny + idx[2];
    indexes[1] = idxx[0]*nyz + idx[1]*ny + idx[2];
    indexes[2] = idx[0]*nyz + idxx[1]*ny + idx[2];
    indexes[3] = idxx[0]*nyz + idxx[1]*ny + idx[2];
    indexes[4] = idx[0]*nyz + idx[1]*ny + idxx[2];
    indexes[5] = idxx[0]*nyz + idx[1]*ny + idxx[2];
    indexes[6] = idx[0]*nyz + idxx[1]*ny + idxx[2];
    indexes[7] = idxx[0]*nyz + idxx[1]*ny + idxx[2];
    

    for (int comp=0; comp<c->iparams[0]; comp++) {
	
	data = (double*)c->vpparams[comp]; //data pointer to the component

    printf("Check1 \n");

    printf("\n");
    printf("max = %i\n", 78*27*147);
    printf("0 0 0 %i \n", indexes[0]);
    printf("1 0 0 %i \n", indexes[1]);
    printf("0 1 0 %i \n", indexes[2]);
    printf("1 1 0 %i \n", indexes[3]);
    printf("0 0 1 %i \n", indexes[4]);
    printf("1 0 1 %i \n", indexes[5]);
    printf("0 1 1 %i \n", indexes[6]);
    printf("1 1 1 %i \n", indexes[7]);
    printf("\n");

	for (int i = 0; i < 4; i++){
        //SEG FAULTS HERE
        printf("%i %i \n",i , indexes[2*i] );
	    C000[i] = (1.0-t[0])*data[ indexes[2*i] ] + t[0]*data[ indexes[2*i+1] ];
    }


	
	C000[0] = C000[0]*(1.0-t[1]) + C000[1]*t[1];
	C000[1] = C000[2]*(1.0-t[1]) + C000[3]*t[1];
	
	C000[0] = C000[0]*(1.0-t[2]) + C000[1]*t[2];
	


	GlobalBuffers[c->outputs[comp]] = C000[0];
    }
        printf("Check2\n");
        printf("\n");
}



/******************************************************
 * inputs[0] = coordinate x
 * outputs[0-dim-1] = interpolated vector field
 * params[0] = dx grid step
 * params[1] = size of box
 * iparams[0] = number of points
 * iparams[1] = number of components
 * iparams[2] = periodic 0|1
 * ***************************************************/
int Add_i1Dlin( int owner, int components, double dx, int pbc) {
	
    circuit c = NewCircuit();

    c.nI = 1;
    c.nO = components;
	
	c.plen = 2;
	c.params = (double*)calloc(c.plen,sizeof(double));
	c.params[0] = dx;
	c.params[1] = dx*2;
	
	c.iplen = 2;
	c.iparams = (int*)calloc(c.iplen,sizeof(int));
	c.iparams[0] = 2;
	c.iparams[1] = components;
	c.iparams[2] = pbc;
	
	c.vplen = components;
	c.vpparams = (void**)malloc(c.vplen*sizeof(double*));
	for (int i = 0; i < c.vplen; i++) {
		c.vpparams[i] = (double*)calloc(2,sizeof(double)); //this contains the data - just 2 points
	}
	
    c.updatef = i1Dlin_periodic;
    
    int index = AddToCircuits(c,owner);
    
    printf("cCore: Added 1D interpolator.\n");
    return index;
	
}
void i1Dlin_SetData(int index, int c, double* data, int npts) {
	
	circuits[index].iparams[0] = npts;
	circuits[index].params[1] = npts*circuits[index].params[0];
	
	//reallocate with the correct size
	circuits[index].vpparams[c] = realloc(circuits[index].vpparams[c],npts*sizeof(double));
	//easy pointer that is the same as vpparams, but itz double*
	double *writer = (double*)circuits[index].vpparams[c];
	
	for(int i=0; i<npts; i++) {
		writer[i] = data[i];
	}
}
void i1Dlin_periodic(circuit* c) {
	
	double x = GlobalSignals[c->inputs[0]];
	x -= floor(x/c->params[1])*c->params[1]; //pbc 
	
	/*else {
		if(x > c->iparams[0]*c->params[0]) {
			for (int i = 0; i < c->iparams[1]; i++) {
				GlobalBuffers[c->outputs[i]] = 0;
			}
		}
	}*/
	
	int idx = floor(x/c->params[0]); //index of the left gridpoint
	int idxp= idx+1; //index of the right gridpoint
	if (idxp == c->iparams[0]) {
		idxp = 0; //take the first 
	}
	
	double t = idx*c->params[0]; //position of left gridpoint
	t = (x-t)/c->params[0]; // interpolation coordinate
	
	double result, *w;
	for (int i = 0; i < c->iparams[1]; i++) {
		w = (double*)c->vpparams[i];
		
		result = t*w[idxp] + (1.0-t)*w[idx];
		GlobalBuffers[c->outputs[i]] = result;
	}
	
	//printf("interpolation: %lf %d \n",x,idx);
	
}




/////////////////////////////////////////////////////////////////
//iparams[0] = components
//iparams[1] = nx
//iparams[2] = ny
//iparams[3] = nz
//iparams[4] = nv
//iparams[5] = PBCx
//iparams[6] = PBCy
//iparams[7] = PBCz
//iparams[8] = PBCv



//params[0] = dx
//params[1] = dy
//params[2] = dz
//params[3] = dv
//params[4] = Voffset

/////////////////////////////////////////////////////////////////
int Add_i4Dlin( int owner, int components) {
	
    circuit c = NewCircuit();
	c.nI = 4;
    c.nO = components;

    c.updatef = i4Dlin;
    
    c.iplen = 9;
    c.iparams = (int*)calloc(c.iplen,sizeof(int));
    c.iparams[0] = components;



    c.plen = 5;
    c.params = (double*)calloc(c.plen,sizeof(double));
    


    c.vplen = components;
    c.vpparams = (double**)malloc(c.vplen * sizeof(double*));
    for (int i = 0; i < components; i++) {
	c.vpparams[i] = (double*)calloc(1, sizeof(double)); // this is the forcefield
    }


    int index = AddToCircuits(c,owner);
    
    printf("cCore: Added 4D interpolator.\n");
    return index;
	
}

int i4DLinPBC(int c, int PBCx, int PBCy, int PBCz, int PBCv){

	circuits[c].iparams[5] = PBCx;
	circuits[c].iparams[6] = PBCy;
	circuits[c].iparams[7] = PBCz;
    circuits[c].iparams[8] = PBCv;
	return 0;
}

double**  i4Dlin_SetUpData(int c, int nx, int ny , int nz, int nv, double dx, double dy, double dz, double dv, double Voffset){


	    circuits[c].iparams[1] = nx;//number of points
	    circuits[c].iparams[2] = ny;
	    circuits[c].iparams[3] = nz;
	    circuits[c].iparams[4] = nv;

	    circuits[c].params[0] = dx;//step size
	    circuits[c].params[1] = dy;
	    circuits[c].params[2] = dz;
	    circuits[c].params[3] = dv;
        circuits[c].params[4] = Voffset;

	    


        //Allocate memory
	   	for (int i = 0; i < circuits[c].iparams[0]; i++) {
		circuits[c].vpparams[i] = (double*)realloc(circuits[c].vpparams[i],   nv*nx*ny*nz*sizeof(double));
    }

        //Return pointer back to python to fill the array
	    return circuits[c].vpparams;

}

void i4Dlin(circuit* c) {
    double x = GlobalSignals[c->inputs[0]];
    double y = GlobalSignals[c->inputs[1]];
    double z = GlobalSignals[c->inputs[2]];
    double V = GlobalSignals[c->inputs[3]];

    if (V == 0) { V = V +1;}

    int PBCx = c->iparams[5];
	int PBCy = c->iparams[6];
	int PBCz = c->iparams[7];    
    int PBCv = c->iparams[8];

    int oob = 0;

    if (PBCx =! 1 && x >= c->params[0]*c->iparams[1] || x < 0){
        oob = 1;
    }

    if (PBCy =! 1 && y >= c->params[1]*c->iparams[2] || y < 0){
        oob = 1;
    }

    if (PBCz != 1 && z <0){
        oob = 1;
    }

    if (PBCz != 1 && z >= c->params[2]*c->iparams[3]){
        for (int comp=0; comp<c->iparams[0]; comp++){
            
        GlobalBuffers[c->outputs[comp]] = 0;}
        return;   
    }


    if (PBCv =! 1 && V >= c->params[3]*c->iparams[4] || V < 0){
        oob = 1;
    }


    if (oob == 1){
        printf("WARNING i4Dlin OOB!\n");

        for (int comp=0; comp<c->iparams[0]; comp++){
        GlobalBuffers[c->outputs[comp]] = 0;}
        return;
    }


	if (PBCx == 1){
    //Find box the point is in
       
    int BoxNumberx = (int)floor(x/ (c->iparams[1]*c->params[0]) );
    // x - boxNumber-1 * boxsize 
    x = x - (BoxNumberx)* (c->iparams[1]*c->params[0]);
        
	}

	if (PBCy == 1)	{
    int BoxNumbery = (int)floor(y/ (c->iparams[2]*c->params[1]) );
    y = y - (BoxNumbery)* (c->iparams[2]*c->params[1]);
	}

	if (PBCz == 1){
    int BoxNumberz = (int)floor(z/ (c->iparams[3]*c->params[2]) );
    z = z - (BoxNumberz)* (c->iparams[3]*c->params[2]);    
	}

    if (PBCv == 1){
    int BoxNumberV = (int)floor(V/ (c->iparams[4]*c->params[3]) );
    z = z - (BoxNumberV)* (c->iparams[4]*c->params[3]);    
    }

   
    //Since the array starts at 0 this is designed to reduce 
    double Voffset = c->params[4];

    // find lower index points
    int xo = (int)floor(x/c->params[0]); 
    int yo = (int)floor(y/c->params[1]); 
    int zo = (int)floor(z/c->params[2]); 
    int vo = (int)floor((V-Voffset)/c->params[3]);

   
    // find upper indexs of points
    int xi = xo + 1; 
    int yi = yo + 1; 
    int zi = zo + 1;     
    int vi = vo + 1; 


    //Find differences
    double xdo = (x-xo*c->params[0])/(xi*c->params[0]-xo*c->params[0]);
    double ydo = (y-yo*c->params[1])/(yi*c->params[1]-yo*c->params[1]);
    double zdo = (z-zo*c->params[2])/(zi*c->params[2]-zo*c->params[2]);
    double vdo = (V-(vo*c->params[3]+Voffset))/( (vi*c->params[3]+Voffset)-(vo*c->params[3]+Voffset));
 
//    printf("%f %f %f %f \n",V,vo*c->params[3]+Voffset, vi*c->params[3]+Voffset );
   // printf("%f %f %f\n", xdo,ydo,zdo);

    


///////////////////////////////////////////////////////////////////////////////////
    //Find value for lower field

    //Loop over al components 

    for (int i = 0; i < c->iparams[0]; i++) {
    //Set up pointer to array
    double *datao;
    datao = (double*)c->vpparams[i];


    //Index = i + J*sizeI + k*sizei*sizej + V*Vsize
    int Index000 = xo + yo*c->iparams[1] + zo*c->iparams[1]*c->iparams[2] + vo*c->iparams[1]*c->iparams[2]*c->iparams[3];
    int Index010 = xo + yi*c->iparams[1] + zo*c->iparams[1]*c->iparams[2] + vo*c->iparams[1]*c->iparams[2]*c->iparams[3];
    int Index001 = xo + yo*c->iparams[1] + zi*c->iparams[1]*c->iparams[2] + vo*c->iparams[1]*c->iparams[2]*c->iparams[3];
    int Index011 = xo + yi*c->iparams[1] + zi*c->iparams[1]*c->iparams[2] + vo*c->iparams[1]*c->iparams[2]*c->iparams[3];
    int Index100 = xi + yo*c->iparams[1] + zo*c->iparams[1]*c->iparams[2] + vo*c->iparams[1]*c->iparams[2]*c->iparams[3];
    int Index110 = xi + yi*c->iparams[1] + zo*c->iparams[1]*c->iparams[2] + vo*c->iparams[1]*c->iparams[2]*c->iparams[3];
    int Index101 = xi + yo*c->iparams[1] + zi*c->iparams[1]*c->iparams[2] + vo*c->iparams[1]*c->iparams[2]*c->iparams[3];
    int Index111 = xi + yi*c->iparams[1] + zi*c->iparams[1]*c->iparams[2] + vo*c->iparams[1]*c->iparams[2]*c->iparams[3];


    /*
    printf("000 %f Line Number %i \n",datao[Index000], Index000+263);
    printf("010 %f Line Number %i \n",datao[Index010], Index010+263);
    printf("001 %f Line Number %i \n",datao[Index001], Index001+263);
    printf("011 %f Line Number %i \n",datao[Index011], Index011+263);   
    printf("100 %f Line Number %i \n",datao[Index100], Index100+263);
    printf("110 %f Line Number %i \n",datao[Index110], Index110+263);
    printf("101 %f Line Number %i \n",datao[Index101], Index101+263);
    printf("111 %f Line Number %i \n",datao[Index111], Index111+263);
    */

    double coo = datao[Index000]*(1-xdo) + datao[Index100]*xdo;
    double cio = datao[Index010]*(1-xdo) + datao[Index110]*xdo;
    double coi = datao[Index001]*(1-xdo) + datao[Index101]*xdo;
    double cii = datao[Index011]*(1-xdo) + datao[Index111]*xdo;

    double co = coo*(1-ydo) + cio*ydo;
    double ci = coi*(1-ydo) + cii*ydo;

    double Field1 = co*(1-zdo) + ci*zdo;

   // printf("%f \n",Field1);
///////////////////////////////////////////////////////////////////////////////////




///////////////////////////////////////////////////////////////////////////////////

    //Find value for Upper field



    //Index = i + J*sizeI + k*sizei*sizej + V*Vsize
     Index000 = xo + yo*c->iparams[1] + zo*c->iparams[1]*c->iparams[2] + vi*c->iparams[1]*c->iparams[2]*c->iparams[3];
     Index010 = xo + yi*c->iparams[1] + zo*c->iparams[1]*c->iparams[2] + vi*c->iparams[1]*c->iparams[2]*c->iparams[3];
     Index001 = xo + yo*c->iparams[1] + zi*c->iparams[1]*c->iparams[2] + vi*c->iparams[1]*c->iparams[2]*c->iparams[3];
     Index011 = xo + yi*c->iparams[1] + zi*c->iparams[1]*c->iparams[2] + vi*c->iparams[1]*c->iparams[2]*c->iparams[3];
     Index100 = xi + yo*c->iparams[1] + zo*c->iparams[1]*c->iparams[2] + vi*c->iparams[1]*c->iparams[2]*c->iparams[3];
     Index110 = xi + yi*c->iparams[1] + zo*c->iparams[1]*c->iparams[2] + vi*c->iparams[1]*c->iparams[2]*c->iparams[3];
     Index101 = xi + yo*c->iparams[1] + zi*c->iparams[1]*c->iparams[2] + vi*c->iparams[1]*c->iparams[2]*c->iparams[3];
     Index111 = xi + yi*c->iparams[1] + zi*c->iparams[1]*c->iparams[2] + vi*c->iparams[1]*c->iparams[2]*c->iparams[3];


    /*
    printf("000 %f Line Number %i \n",datao[Index000], Index000 - 9720000 +263);
    printf("010 %f Line Number %i \n",datao[Index010], Index010 - 9720000 +263);
    printf("001 %f Line Number %i \n",datao[Index001], Index001 - 9720000 +263);
    printf("011 %f Line Number %i \n",datao[Index011], Index011 - 9720000 +263);   
    printf("100 %f Line Number %i \n",datao[Index100], Index100 - 9720000 +263);
    printf("110 %f Line Number %i \n",datao[Index110], Index110 - 9720000 +263);
    printf("101 %f Line Number %i \n",datao[Index101], Index101 - 9720000 +263);
    printf("111 %f Line Number %i \n",datao[Index111], Index111 - 9720000 +263);
    */


     coo = datao[Index000]*(1-xdo) + datao[Index100]*xdo;
     cio = datao[Index010]*(1-xdo) + datao[Index110]*xdo;
     coi = datao[Index001]*(1-xdo) + datao[Index101]*xdo;
     cii = datao[Index011]*(1-xdo) + datao[Index111]*xdo;

     co = coo*(1-ydo) + cio*ydo;
     ci = coi*(1-ydo) + cii*ydo;

    double Field2 = co*(1-zdo) + ci*zdo;

   // printf("%f \n",Field2);  

///////////////////////////////////////////////////////////////////////////////////
	//Interpolate across the fields
    double Field3 = Field1*(1-vdo) + Field2*vdo;
   // printf("%f %f\n ", Field3, vdo); 
   GlobalBuffers[c->outputs[i]] = Field3; 
    }

}