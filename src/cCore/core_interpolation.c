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
	
    //printf("asd! %lf %lf %lf\n",pos[0],pos[1],pos[2]);
    //printf("asd! %lf %lf %lf\n",t[0],t[1],t[2]);
    //printf("asd! %d %d %d\n",idx[0],idx[1],idx[2]);
    //printf("asd! %d %d %d\n",idxx[0],idxx[1],idxx[2]);
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
	
	for (int i = 0; i < 4; i++)
	    C000[i] = (1.0-t[0])*data[ indexes[2*i] ] + t[0]*data[ indexes[2*i+1] ];
	
	C000[0] = C000[0]*(1.0-t[1]) + C000[1]*t[1];
	C000[1] = C000[2]*(1.0-t[1]) + C000[3]*t[1];
	
	C000[0] = C000[0]*(1.0-t[2]) + C000[1]*t[2];
	
	GlobalBuffers[c->outputs[comp]] = C000[0];
    }

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


