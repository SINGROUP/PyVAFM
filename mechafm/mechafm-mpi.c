/****************************
 **                        **
 **  Mechanical AFM Model  **
 **                        **
 **   Hapala et al, PRB    **
 **    90:085421 (2014)    **
 **                        **
 **  ANSI C Implementation **
 **    (c) P. Spijker      **
 **                        **
 ****************************/

/* Load system headers */
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>
#include <glob.h>
#include <mpi.h>
#include <sys/time.h>

/* Some macro definitions */
#define LINE_LENGTH 512
#define NAME_LENGTH 128
#define ATOM_LENGTH 8
#define TOLERANCE 1e-10
#define TRUE 1
#define FALSE 0
#define PI 3.14159265358979323846
#define SIXTHRT2 1.12246204830937298142

/* Local definitions */

/* Define vector types */
typedef struct vector {
  double x, y, z;
} VECTOR;
VECTOR NULL_vector = {0.0,0.0,0.0};
typedef struct ivector {
  int x, y, z;
} IVECTOR;
IVECTOR NULL_ivector = {0,0,0};

/* Define a structure for all input options */
typedef struct InputOptions {
  char xyzfile[NAME_LENGTH];
  char paramfile[NAME_LENGTH];
  char tipatom[NAME_LENGTH];
  char dummyatom[NAME_LENGTH];
  char planeatom[NAME_LENGTH];
  double dx, dy, dz;
  double zlow, zhigh;
  int coulomb;
  int maxsteps, minterm;
  double etol, ftol, cfac;
  int bufsize;
} InputOptions;

/* Define a structure to quickly compute nonbonded interactions */
typedef struct InteractionList {
  double es12;
  double es6;
  double qq;
  double k;
  double r0;
  double rmin;
} InteractionList;

/* Define a structure for easy processor communication */
typedef struct buffer {
  int ix, iy, iz, n;
  double angle, e, vv;
  VECTOR pos, f, v;
} BUFFER;

/* A simple list to distinguish different minimization criteria */
enum{MIN_E,MIN_F,MIN_EF}; 

/* Time thingies */
struct timeval TimeStart, TimeEnd;

/**********************
 ** GLOBAL VARIABLES **
 **********************/

char InputFileName[NAME_LENGTH];   /* File name of the input file */
InputOptions Options;              /* Structure containing all relevant input options */
int Natoms;                        /* Number of surface atoms */
VECTOR *Surf_pos;                  /* Vector containing positions of all surface atoms */
double *Surf_q;                    /* List containing charges of all surface atoms */
char **Surf_types;                 /* List containing types of all surface atoms */
VECTOR Box;                        /* Vector containing the size of the universe */
InteractionList *CrossParams;      /* Structured list for all cross particle interaction parameters */
InteractionList DummyParams;       /* List for particle interaction parameters with dummy atom */
InteractionList Harmonic;          /* List for the harmonic constraint paramets on the tip atom */
VECTOR Tip_pos;                    /* Position of the tip atom */
VECTOR Dummy_pos;                  /* Position of the dummy atom */
VECTOR TipSurf_force;              /* Force on tip atom caused by the surface */
VECTOR TipDummy_force;             /* Force on tip atom caused by the dummy atom */ 
VECTOR TipHarmonic_force;          /* Force on tip atom caused by the harmonic constraint */
double TipSurf_energy;             /* Energy of tip atom caused by the surface */
double TipDummy_energy;            /* Energy of tip atom caused by the dummy atom */
double TipHarmonic_energy;         /* Energy of tip atom caused by the harmonic constraint */
IVECTOR Npoints;                   /* Number of points (x,y,z) for the tip */
int Ntotal;                        /* Total number of minimization loops used */
FILE **FStreams;                   /* Array with the entire file stream */

/* Some parallel specific global variables */
MPI_Comm Universe;                 /* The entire parallel universe */
int NProcessors;                   /* Total number of processors */
int Me;                            /* The current processor */
int RootProc;                      /* The main processor */               
int *PointsOnProc;                 /* How many x,y points on this processor */

/**********************
 ** HEADER FUNCTIONS **
 **********************/

/* An error function */
void error(char *message, ...) { 
  va_list arg;
  static char ws[LINE_LENGTH];
  va_start(arg, message);
  vsprintf(ws, message, arg);
  va_end(arg);
  fprintf(stderr, "+- ERROR (on proc %d): %s\n", Me, ws);
  MPI_Finalize();
  exit(1);
}

/* Print some debug information to the screen */
void debugline(int proc, char *message, ...) {
  va_list arg;
  static char ws[LINE_LENGTH];
  va_start(arg, message);
  vsprintf(ws, message, arg);
  va_end(arg);
  if (Me==proc) { fprintf(stdout, "+- %s\n", ws); }
}

/* A sort function */
int compare(const void * a, const void * b) {
  return ( *(int*)a - *(int*)b );
}

/* Convert a string to uppercase */
char *strupp(char *string) {
  char *convert;
  convert = string;
  do { *convert = toupper((unsigned char)*convert); } while (*convert++);
  return string;
}

/* Convert a string to lowercase */
char *strlow(char *string) {
  char *convert;
  convert = string;
  do { *convert = tolower((unsigned char)*convert); } while (*convert++);
  return string;
}
  
/* Filter out comment and empty lines in a file */
int checkForComments(char *line) {
  int moveon = FALSE;
  if (line[0] == '#') { moveon = TRUE; }
  else if (line[0] == '%') { moveon = TRUE; }
  else if (line[0] == '\n') { moveon = TRUE; }
  return moveon;
}

/**************************
 ** FILE INPUT FUNCTIONS **
 **************************/

/* Read stuff from the command line */
void parseCommandLine(int argc, char *argv[]) {
  if (Me==RootProc) {
    fprintf(stdout,"+ - - - - - - - - - - - - - - - - - - - - - - - - - +\n");
    fprintf(stdout,"| Mechanical AFM Model by Hapala et al, PRB (2014)  |\n");
    fprintf(stdout,"|    This MPI-C implemenation by P. Spijker         |\n");
    fprintf(stdout,"+ - - - - - - - - - - - - - - - - - - - - - - - - - +\n");
  }
  if ((argc < 2) || (argc > 2)) { error("Specify an input file to be read!"); }
  else { sprintf(InputFileName,"%s",argv[1]); }
  return;
}

/* A function to read an input file */
void readInputFile(void) {
  
  FILE *fp;
  char keyword[NAME_LENGTH];
  char value[NAME_LENGTH];
  char line[LINE_LENGTH];
  char tmp_coulomb[NAME_LENGTH], tmp_minterm[NAME_LENGTH];
  
  /* Initialize the mandatory options */
  sprintf(Options.xyzfile,"");
  sprintf(Options.paramfile,"");
  sprintf(Options.tipatom,"");
  sprintf(Options.dummyatom,"");  
  sprintf(Options.planeatom,"");
  Options.minterm = -1;

  /* Initialize the other options */
  Options.coulomb = FALSE;
  Options.dx = 0.1;
  Options.dy = 0.1;
  Options.dz = 0.1;
  Options.zlow = 6.0;
  Options.zhigh = 10.0;
  Options.etol = 0.01;
  Options.ftol = 0.01;
  Options.cfac = 0.001;
  Options.maxsteps = 5000;
  Options.bufsize = 1000;

  /* Check if the file exists */
  fp = fopen(InputFileName,"r");
  if (fp==NULL) { error("The file %s does not exist!",InputFileName); }
  
  /* Scan the file line by line */
  while (fgets(line, LINE_LENGTH, fp)!=NULL) {
    /* Skip empty and commented lines */
    if (checkForComments(line)) { continue; }
    /* Get the keyword and convert to uppercase */
    sscanf(line, "%s %s", keyword, value);
    strlow(keyword);
    if (strcmp(keyword,"xyzfile")==0) { sprintf(Options.xyzfile,"%s",value); } 
    else if (strcmp(keyword,"paramfile")==0) { sprintf(Options.paramfile,"%s",value); } 
    else if (strcmp(keyword,"tipatom")==0) { sprintf(Options.tipatom,"%s",value); } 
    else if (strcmp(keyword,"dummyatom")==0) { sprintf(Options.dummyatom,"%s",value); } 
    else if (strcmp(keyword,"planeatom")==0) { sprintf(Options.planeatom,"%s",value); } 
    else if (strcmp(keyword,"dx")==0) { Options.dx = atof(value); }
    else if (strcmp(keyword,"dy")==0) { Options.dy = atof(value); }
    else if (strcmp(keyword,"dz")==0) { Options.dz = atof(value); }
    else if (strcmp(keyword,"zlow")==0) { Options.zlow = atof(value); }
    else if (strcmp(keyword,"zhigh")==0) { Options.zhigh = atof(value); }
    else if (strcmp(keyword,"etol")==0) { Options.etol = atof(value); }
    else if (strcmp(keyword,"ftol")==0) { Options.ftol = atof(value); }
    else if (strcmp(keyword,"cfac")==0) { Options.cfac = atof(value); }
    else if (strcmp(keyword,"maxsteps")==0) { Options.maxsteps = atoi(value); }
    else if (strcmp(keyword,"bufsize")==0) { Options.bufsize = atoi(value); }
    else if (strcmp(keyword,"coulomb")==0) { 
      if (strcmp(value,"on")==0) { Options.coulomb = TRUE; }
      else if (strcmp(value,"on")==0) { Options.coulomb = FALSE; }
      else { error("Option %s must be either on or off!", keyword); }
    }
    else if (strcmp(keyword,"minterm")==0) { 
      if (strcmp(value,"e")==0) { Options.minterm = MIN_E; }
      else if (strcmp(value,"f")==0) { Options.minterm = MIN_F; }
      else if (strcmp(value,"ef")==0) { Options.minterm = MIN_EF; }
      else { error("Option %s must be either e, f or ef!", keyword); }
      sprintf(tmp_minterm,"%s",value);
    }
    else { error("Unknown option %s!", keyword); }
  }

  /* Check if all necessary options are initialized */
  if (strcmp(Options.xyzfile,"")==0) { error("Specify at least an xyzfile!"); }
  if (strcmp(Options.paramfile,"")==0) { error("Specify at least a parameter file!"); }  
  if (strcmp(Options.tipatom,"")==0) { error("Specify at least a tip atom!"); }
  if (strcmp(Options.dummyatom,"")==0) { error("Specify at least a dummy atom!"); }  
  if (strcmp(Options.planeatom,"")==0) { error("Specify at least a plane atom!"); }  
  if (Options.minterm<0) { error("Specify at least a minimization termination criterion (e, f, or ef)!"); }

  /* Close file */
  fclose(fp);

  /* Set some useful thingies */
  if (Options.coulomb) { sprintf(tmp_coulomb,"%s","on"); }
  else { sprintf(tmp_coulomb,"%s","off"); }

  /* Talk to me */
  debugline(RootProc,"");
  debugline(RootProc,"Input settings for %s:", InputFileName);
  debugline(RootProc,"");
  debugline(RootProc,"xyzfile:     %-s", Options.xyzfile);
  debugline(RootProc,"paramfile:   %-s", Options.paramfile);
  debugline(RootProc,"tipatom:     %-s", Options.tipatom);
  debugline(RootProc,"dummyatom:   %-s", Options.dummyatom);
  debugline(RootProc,"planeatom:   %-s", Options.planeatom);
  debugline(RootProc,"");
  debugline(RootProc,"minterm:     %-s", tmp_minterm);
  debugline(RootProc,"etol:        %-8.4f", Options.etol);
  debugline(RootProc,"ftol:        %-8.4f", Options.ftol);
  debugline(RootProc,"cfac:        %-8.4f", Options.cfac);
  debugline(RootProc,"maxsteps:    %-8d", Options.maxsteps);
  debugline(RootProc,"");
  debugline(RootProc,"zhigh:       %-8.4f", Options.zhigh);
  debugline(RootProc,"zlow:        %-8.4f", Options.zlow);
  debugline(RootProc,"dx:          %-8.4f", Options.dx);  
  debugline(RootProc,"dy:          %-8.4f", Options.dy);
  debugline(RootProc,"dz:          %-8.4f", Options.dz);
  debugline(RootProc,"");
  debugline(RootProc,"coulomb:     %-s",tmp_coulomb);
  debugline(RootProc,"");
  debugline(RootProc,"bufsize:     %-8d", Options.bufsize);
  debugline(RootProc,"");

  /* Return home */
  return;
}

/* Read the XYZ file */
void readXYZFile(void) {
  
  FILE *fp;
  int i, nplaneatoms;
  char line[LINE_LENGTH];
  double avgz;

  /* Read the file once, to determine the number of atoms */
  fp = fopen(Options.xyzfile,"r");
  if (fp==NULL) { error("No such file: %s!", Options.xyzfile); }
  Natoms = 0;
  while (fgets(line, LINE_LENGTH, fp)!=NULL) {
    /* Skip empty and commented lines */
    if (checkForComments(line)) { continue; }
    /* Count useful lines */
    Natoms++;
  }
  rewind(fp);

  /* Initialize the global surface atoms vector and lists */
  Surf_pos = (VECTOR *)malloc(Natoms*sizeof(VECTOR));
  Surf_q = (double *)malloc(Natoms*sizeof(double));
  Surf_types = (char **)malloc(Natoms*sizeof(char*));
  for (i=0; i<Natoms; ++i) { Surf_types[i] = (char *)malloc(ATOM_LENGTH*sizeof(char)); }

  /* Read each line and store the data */
  i = 0;
  while (fgets(line, LINE_LENGTH, fp)!=NULL) {
    /* Skip empty and commented lines */
    if (checkForComments(line)) { continue; }
    /* Read line */
    sscanf(line, "%s %lf %lf %lf %lf", Surf_types[i], &(Surf_pos[i].x), &(Surf_pos[i].y), &(Surf_pos[i].z), &(Surf_q[i]));
    i++;
  }

  /* Put the plane atoms at 0 (in z) */
  avgz = 0.0;
  nplaneatoms = 0;
  for (i=0; i<Natoms; ++i) {
    if (strcmp(Surf_types[i],Options.planeatom)==0) {
      nplaneatoms++;
      avgz += Surf_pos[i].z;
    }
  }
  avgz /= nplaneatoms;
  for (i=0; i<Natoms; ++i) { Surf_pos[i].z -= avgz; }

  /* Return home */
  return;
}

/* Mixing rule functions */
double mixsig(double sig1, double sig2) { return (sig1+sig2)/2; }
double mixeps(double eps1, double eps2) { return sqrt(eps1*eps2); }

/* Read the parameter file */
void readParameterFile(void) {

  FILE *fp;
  char atom[ATOM_LENGTH], keyword[NAME_LENGTH], dump[NAME_LENGTH], line[LINE_LENGTH];
  double eps, sig, eps_cross, sig_cross;
  double eps_tip, sig_tip, q_tip, qbase;
  int i, check, hcheck, nplaneatoms, natoms;
  double avgx, avgy, dx, dy;

  /* Initialize the universe */
  Box.x = Box.y = Box.z = -1.0;

  /* Open the parameter file */
  fp = fopen(Options.paramfile,"r");
  if (fp==NULL) { error("No parameter file %s found!",Options.paramfile); }

  /* Scan the parameter file for the universe size and for the tip atom definitions */
  check = FALSE;
  while (fgets(line, LINE_LENGTH, fp)!=NULL) {
    /* Skip empty and commented lines */
    if (checkForComments(line)) { continue; }
    /* Read line to determine keyword */
    sscanf(line,"%s",keyword);
    /* Process the separate keywords */
    if (strcmp(keyword,"box")==0) {
      if ( (Box.x<0) && (Box.y<0) && (Box.z<0)) { sscanf(line,"%s %lf %lf %lf",dump,&(Box.x),&(Box.y),&(Box.z)); }
      else { error("Keyword box cannot be defined more than once in parameter file!"); }
    }
    if (strcmp(keyword,"atom")==0) {
      sscanf(line,"%s %s",dump,atom);
      if (strcmp(atom,Options.tipatom)==0) {
	if (check == TRUE) { error("Parameters for tip atom can only be specified once!"); }
	sscanf(line,"%s %s %lf %lf %s %lf",dump,dump,&(eps_tip),&(sig_tip),dump,&(q_tip));
	check = TRUE;
      }
    }
  }
  if (!check) { error("Parameters for tip atom not defined in parameter file!"); } 
  rewind(fp);

  /* Now we know the size of the universe, put the molecule in the center of it */
  avgx = avgy = 0.0;
  nplaneatoms = 0;
  for (i=0; i<Natoms; ++i) {
    if (strcmp(Surf_types[i],Options.planeatom)==0) {
      nplaneatoms++;
      avgx += Surf_pos[i].x;
      avgy += Surf_pos[i].y;
    }
  }
  avgx /= nplaneatoms;
  avgy /= nplaneatoms;
  dx = (Box.x/2) - avgx;
  dy = (Box.y/2) - avgy;
  for (i=0; i<Natoms; ++i) { 
    Surf_pos[i].x += dx;
    Surf_pos[i].y += dy;
  }

  /* Set up the interaction list */
  CrossParams = (InteractionList *)malloc(Natoms*sizeof(InteractionList));

  /* The constant part of the Coulomb equation */
  qbase = 332.0636 / 1.0;

  /* Read the parameter file again, but this time, create the interaction list 
     for the surface atoms, for the dummy atom, and also for the harmonic spring */
  check = hcheck = FALSE;
  natoms = 0;  
  while (fgets(line, LINE_LENGTH, fp)!=NULL) {
    /* Skip empty and commented lines */
    if (checkForComments(line)) { continue; }
    /* Read line to determine keyword */
    sscanf(line,"%s",keyword);
    if (strcmp(keyword,"atom")==0) {
      sscanf(line,"%s %s %lf %lf",dump,atom,&(eps),&(sig));
      /* Loop all atoms in the surface and check if they match this parameter set */
      for (i=0; i<Natoms; ++i) {
	if (strcmp(Surf_types[i],atom)==0) {
	  natoms++;
	  eps_cross = mixeps(eps,eps_tip);
	  sig_cross = mixsig(sig,sig_tip);              /* To power 1 */
	  sig_cross = (sig_cross*sig_cross*sig_cross);  /* To power 3 */
	  sig_cross *= sig_cross;                       /* To power 6 */
	  CrossParams[i].es12 = 4 * eps_cross * sig_cross * sig_cross;
	  CrossParams[i].es6  = 4 * eps_cross * sig_cross;
	  CrossParams[i].qq   = qbase * q_tip * Surf_q[i];
	}
      }
      /* We found a dummy atom in the parameter list */
      if (strcmp(Options.dummyatom,atom)==0) {
	if (check == TRUE) { error("Parameters for dummy atom can only be specified once!"); }
	check = TRUE;
	eps_cross = mixeps(eps,eps_tip);
	sig_cross = mixsig(sig,sig_tip);              /* To power 1 */
	sig_cross = (sig_cross*sig_cross*sig_cross);  /* To power 3 */
	sig_cross *= sig_cross;                       /* To power 6 */
	DummyParams.es12 = 4 * eps_cross * sig_cross * sig_cross;
	DummyParams.es6  = 4 * eps_cross * sig_cross;
	DummyParams.qq   = 0.0; /* Ignore Coulomb interaction between tip and dummy */
	DummyParams.rmin = mixsig(sig,sig_tip) * SIXTHRT2; /* Needed for tip positioning */
      }
    }
    if (strcmp(keyword,"harm")==0) {
      if (hcheck == TRUE) { error("Parameters for harmonic spring can only be specified once!"); }
      sscanf(line,"%s %s %lf %lf",dump,atom,&(Harmonic.k),&(Harmonic.r0));
      if (strcmp(atom,Options.tipatom)!=0) { error("Harmonic spring should be defined on tip atom!"); }
      hcheck = TRUE;
    }
  }
  if (natoms != Natoms) { error("Not all atoms have been assigned parameters!"); }
  if (check == FALSE) { error("Parameters for dummy atom not defined in parameter file!"); }
  if (hcheck == FALSE) { error("No harmonic spring parameters found in parameter file!"); }

  /* Close file */
  fclose(fp);

  /* Return home */
  return;
}

/***************************
 ** INTERACTION FUNCTIONS **
 ***************************/

/* Interaction between tip and surface */
void interactTipSurface(void) {

  int i;
  double dx, dy, dz, rsqt, r;
  double e, fx, fy, fz;
  double fpair, terma, termb, termc, sr6, sr12;
  
  /* Zero the forces and energy */
  TipSurf_energy = 0.0;
  TipSurf_force = NULL_vector;

  /* Loop all surface particles */
  for (i=0; i<Natoms; ++i) {
    /* Compute distance (components) */
    dx = Tip_pos.x - Surf_pos[i].x;
    dy = Tip_pos.y - Surf_pos[i].y;
    dz = Tip_pos.z - Surf_pos[i].z;
    rsqt = dx*dx + dy*dy + dz*dz;
    /* The Lennard-Jones interaction coefficients */
    sr6 = rsqt*rsqt*rsqt;
    sr12 = sr6*sr6;
    terma = CrossParams[i].es12/sr12;
    termb = CrossParams[i].es6/sr6;
    fpair = (12*terma-6*termb)/rsqt;
    /* The Coulomb interaction coefficients (only if coulomb is on) */
    if (Options.coulomb) { termc = CrossParams[i].qq/sqrt(rsqt); }
    else { termc = 0.0; }
    /* The interaction energy */
    TipSurf_energy += (terma - termb) + termc;
    /* The interaction force */
    TipSurf_force.x += (fpair+(termc/rsqt))*dx;
    TipSurf_force.y += (fpair+(termc/rsqt))*dy;
    TipSurf_force.z += (fpair+(termc/rsqt))*dz;
  }

  /* Go home */
  return;
}
  
/* Interaction between tip and dummy atom */
void interactTipDummy(void) {

  double dx, dy, dz, rsqt, r;
  double fpair, terma, termb, termc, sr6, sr12;

  /* Compute distance (components) */
  dx = Tip_pos.x - Dummy_pos.x;
  dy = Tip_pos.y - Dummy_pos.y;
  dz = Tip_pos.z - Dummy_pos.z;
  rsqt = dx*dx + dy*dy + dz*dz;
  /* The Lennard-Jones interaction coefficients */
  sr6 = rsqt*rsqt*rsqt;
  sr12 = sr6*sr6;
  terma = DummyParams.es12/sr12;
  termb = DummyParams.es6/sr6;
  fpair = (12*terma-6*termb)/rsqt;
  /* The interaction energy */
  TipDummy_energy = (terma - termb);
  /* The interaction force */
  TipDummy_force.x = fpair*dx;
  TipDummy_force.y = fpair*dy;
  TipDummy_force.z = fpair*dz;

  /* Go home */
  return;
}
  
/* Interaction between tip and harmonic constraint */
void interactTipHarmonic(void) {
  
  double dx, dy, r, dr, rk, fharm;
  
  /* Compute distance (components, but not in z!) */
  dx = Tip_pos.x - Dummy_pos.x;
  dy = Tip_pos.y - Dummy_pos.y;
  r = sqrt(dx*dx + dy*dy);
  /* Compute the harmonic coefficients */
  dr = r - Harmonic.r0;
  rk = Harmonic.k*dr;
  /* The interaction energy */
  TipHarmonic_energy = rk*dr;
  /* The interaction force */
  if (r>TOLERANCE) { fharm = (-2*rk/r); }
  else { fharm = 0.0; }
  TipHarmonic_force.x = fharm*dx;
  TipHarmonic_force.y = fharm*dy;
  TipHarmonic_force.z = 0.0;

  /* Go home */
  return;
}

/***************************
 ** FILE OUTPUT FUNCTIONS **
 ***************************/

void dumpToFiles(BUFFER *sendbuf, BUFFER *recvbuf, int bufsize) {

  int i, f, nsr, *curbufsize, *lcbs;
  MPI_Status mpistatus;

  /* Build an array of the current buffer size for broadcast */
  curbufsize = (int *)malloc(NProcessors*sizeof(int));
  lcbs = (int *)malloc(NProcessors*sizeof(int));
  for (i=0; i<NProcessors; ++i) { lcbs[i] = 0; }
  lcbs[Me] = bufsize;
  MPI_Allreduce(lcbs,curbufsize,NProcessors,MPI_INT,MPI_SUM,Universe);

  /* Send the data to the root processor */
  if (Me != RootProc) { MPI_Send(sendbuf,curbufsize[Me]*sizeof(BUFFER),MPI_CHAR,RootProc,0,Universe); }
  /* Receive the date from the daughter processors and write to file */
  else {
    /* Loop the processors */
    for (i=0; i<NProcessors; ++i) {
      /* On the main processor we have to copy the data only, no send and receive */      
      if (i==0) { recvbuf = sendbuf; }
      /* For all other processors we need to receive the data */
      else { MPI_Recv(recvbuf,curbufsize[i]*sizeof(BUFFER),MPI_CHAR,i,0,Universe,&mpistatus); }
      /* Write data to file (only the root processor can do this) */
      /* PLEASE NOTE: DATA IS SENT IN STRIPED FORM, THEY ARE NOT ORDERED! */
      for (nsr=0; nsr<curbufsize[i]; ++nsr) {
	f = recvbuf[nsr].iz;
	fprintf(FStreams[f],"%d %d %d ",recvbuf[nsr].iz,recvbuf[nsr].ix,recvbuf[nsr].iy);
	fprintf(FStreams[f],"%6.3f %6.3f %6.3f ",recvbuf[nsr].pos.x,recvbuf[nsr].pos.y,recvbuf[nsr].pos.z);
	fprintf(FStreams[f],"%8.4f %8.4f %8.4f ",recvbuf[nsr].f.x,recvbuf[nsr].f.y,recvbuf[nsr].f.z);
	fprintf(FStreams[f],"%6.3f %6.3f %6.3f ",recvbuf[nsr].v.x,recvbuf[nsr].v.y,recvbuf[nsr].v.z);
	fprintf(FStreams[f],"%6.3f %8.4f ",recvbuf[nsr].vv,recvbuf[nsr].angle);
	fprintf(FStreams[f],"%8.4f %d\n",recvbuf[nsr].e,recvbuf[nsr].n);
      }
    }
  }      
    
  /* Get rid of the buffer size broadcast arrays */
  free(curbufsize);
  free(lcbs);

  /* Go home */
  return;
}

/************************************
 ** FREQUENCY SHIFT APPROXIMATIONS **
 ************************************/

void computeDeltaF(double x, double y, VECTOR *ftip) {

  int i;
  double z;

  /* Wait! */
  MPI_Barrier(Universe);

  /* Copy data */
  for (i=0; i<=Npoints.z; ++i) {
    z = Options.zhigh - i*Options.dz;
    fprintf(stdout,"@ %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f\n",x,y,z,ftip[i].x,ftip[i].y,ftip[i].z);
  }
  
  /* Go home */
  return;
}

/*************************************************
 ** EVERYTHING TO DO WITH THE SIMULATION ITSELF **
 *************************************************/

/* Set some global variables we need and open the file streams */
void openUniverse(void) {
  
  int i, n;
  double z;
  char outfile[NAME_LENGTH];

  /* How many points to compute the tip relaxation on */
  Npoints.x = (int)(Box.x/Options.dx);
  Npoints.y = (int)(Box.y/Options.dy);
  Npoints.z = (int)((Options.zhigh-Options.zlow)/Options.dz);
  n = (Npoints.x + 1) * (Npoints.y + 1) * (Npoints.z + 1);
  debugline(RootProc,"3D data grid is: %d x %d x %d (%d in total)",1+Npoints.x,1+Npoints.y,1+Npoints.z,n);

  /* Wait! */
  MPI_Barrier(Universe);

  /* Open all the file streams (one for every z point) [ONLY ON ROOT PROCESSOR] */
  if (Me == RootProc) {
    FStreams = (FILE **)malloc((Npoints.z+1)*sizeof(FILE *));
    for (i=0; i<=Npoints.z; ++i) {
      z = Options.zhigh - i*Options.dz;
      sprintf(outfile,"scan-%06.3f.dat",z);
      FStreams[i] = fopen(outfile,"w");
    }   
  }

  /* Note the time */
  gettimeofday(&TimeStart, NULL);

  /* Go home */
  return;
}

/* Now move the tip! */
void moveTip(void) {

  int n, nmax, check;
  int ix, iy, iz;
  double x, y, z;
  double angle, minangle, maxforce, vv;
  double e, ediff, eold, fnorm;
  VECTOR f, v;
  VECTOR *ftip;
  int nxy, onproc, bufsize, nsr;
  BUFFER *sendbuf, *recvbuf;
  double checkperc, curperc;

  /* Create a force vector (for real time analysis) */
  ftip = (VECTOR *)malloc((Npoints.z+1)*sizeof(VECTOR));

  /* DEBUG DEBUG DEBUG DEBUG DEBUG */
  //Npoints.x = Npoints.y = 10;

  /* Some initialization */
  Ntotal = 0;
  checkperc = curperc = 0.10;
  debugline(RootProc,"Simulation run started now");

  /* Initialize the storage send and receive buffers */
  nxy = (Npoints.x + 1)*(Npoints.y + 1);
  bufsize = Options.bufsize * (Npoints.z+1);
  sendbuf = (BUFFER *)malloc(bufsize*sizeof(BUFFER));
  recvbuf = (BUFFER *)malloc(bufsize*sizeof(BUFFER));
  nsr = 0;

  /* Loop x */
  for (ix=0; ix<=Npoints.x; ++ix) {
    x = ix*Options.dx; /* Current x */
      
    /* Loop y */
    for (iy=0; iy<=Npoints.y; ++iy) {
      y = iy*Options.dy; /* Current y */
      
      /* Check the progress and report every so often */
      n = ix*(Npoints.y+1) + iy;
      if ( (Me == RootProc) && ((((double)n)/(nxy)) >= curperc) ) {
	debugline(RootProc,"Finished approximately %4.1f %% of the simulation",100*curperc);
	curperc += checkperc;
      }

      /* Compute on which processor this x,y combination should be run */
      onproc = n % NProcessors;
      if (onproc != Me) { continue; }
      PointsOnProc[Me]++;

      /* Position the tip far above the surface */
      Dummy_pos.x = x;
      Dummy_pos.y = y;
      Dummy_pos.z = Options.zhigh + Options.dz; /* Plus dz to allow for initial subtraction */
      Tip_pos.x = Dummy_pos.x;
      Tip_pos.y = Dummy_pos.y;
      Tip_pos.z = Dummy_pos.z - DummyParams.rmin;

      /* Approach and optimize */
      nmax = 0;
      minangle = 9e99;
      maxforce = -9e99;
      for (iz=0; iz<=Npoints.z; ++iz) {
	z = Options.zhigh - iz*Options.dz; /* Current z */
      
	/* Move tip and dummy atom toward the surface */
	Dummy_pos.z -= Options.dz;
	Tip_pos.z -= Options.dz;

	/* Collect the force */
	ftip[iz] = NULL_vector;
	
	/* Relax/Minimize the configuration */
	ediff = 5*Options.etol;
	for (n=0; n<Options.maxsteps; ++n) {
	  nmax++;
	  
	  /* Compute all interaction energies */
	  interactTipSurface();
	  interactTipDummy();
	  interactTipHarmonic();

	  /* Total energy and force computed */
	  e = TipSurf_energy + TipDummy_energy + TipHarmonic_energy;
	  f.x = TipSurf_force.x + TipDummy_force.x + TipHarmonic_force.x;
	  f.y = TipSurf_force.y + TipDummy_force.y + TipHarmonic_force.y;
	  f.z = TipSurf_force.z + TipDummy_force.z + TipHarmonic_force.z;
	  fnorm = sqrt(f.x*f.x + f.y*f.y + f.z*f.z);

	  /* Energy difference */
	  if (n>0) { ediff = e - eold; }
	  eold = e;

	  /* Are the forces/energies tolerable */
	  if (Options.minterm == MIN_E) { check = (fabs(ediff)<Options.etol); }
	  else if (Options.minterm == MIN_F) { check = (fabs(fnorm)<Options.ftol); }
	  else if (Options.minterm == MIN_EF) { check = ((fabs(ediff)<Options.etol)&&(fabs(fnorm)<Options.ftol)); }
	  if (check) { break; }
	  
	  /* If they are not tolerable, update position of the tip atom based on the force */
	  Tip_pos.x += Options.cfac * f.x;
	  Tip_pos.y += Options.cfac * f.y;
	  Tip_pos.z += Options.cfac * f.z;
	  
	} /* End minimization loop */
	
	/* Compute some other interesting data */
	v.x = Tip_pos.x - x;
	v.y = Tip_pos.y - y;
	v.z = Tip_pos.z - z;
	vv = sqrt(v.x*v.x + v.y*v.y + v.z*v.z);
	angle = atan2(sqrt(v.x*v.x + v.y*v.y),v.z)*(180.0/PI);
	if (angle<minangle) { minangle = angle; }
	if (fnorm>maxforce) { maxforce = fnorm; }

	/* Collect the final forces on the tip because of the surface */
	ftip[iz].x = TipSurf_force.x;
	ftip[iz].y = TipSurf_force.y;
	ftip[iz].z = TipSurf_force.z;

	/* Store data in send buffers */
	sendbuf[nsr].ix = ix;
	sendbuf[nsr].iy = iy;
	sendbuf[nsr].iz = iz;
	sendbuf[nsr].n  = n;
	sendbuf[nsr].pos.x = x;
	sendbuf[nsr].pos.y = y;
	sendbuf[nsr].pos.z = z;
	sendbuf[nsr].f.x = TipSurf_force.x;
	sendbuf[nsr].f.y = TipSurf_force.y;
	sendbuf[nsr].f.z = TipSurf_force.z;
	sendbuf[nsr].v.x = v.x;
	sendbuf[nsr].v.y = v.y;
	sendbuf[nsr].v.z = v.z;
	sendbuf[nsr].vv = vv;
	sendbuf[nsr].e = TipSurf_energy;
	sendbuf[nsr].angle = angle;
	nsr++;

      } /* End loop in z */

      /* Dump to file (only when the buffer is full, this can and should only happen after a full z approach) */
      if (nsr==bufsize) { dumpToFiles(sendbuf,recvbuf,bufsize); nsr = 0; }

      /* Compute the frequency shift for the given F(z) */
      //computeDeltaF(x,y,ftip);

      /* Talk to me */
      //debugline(Me,"x = %5.2f   y = %5.2f   nmax = %6d   min_angle = %6.2f   max_force = %6.2f",x,y,nmax,minangle,maxforce);

      /* Keep track of counting */
      Ntotal += nmax;

    } /* End loop in y */

  } /* End loop in x */

  /* Dump to file (if it happened that the buffer contains anything at all */
  MPI_Allreduce(&nsr,&n,1,MPI_INT,MPI_SUM,Universe);
  if (n>0) { dumpToFiles(sendbuf,recvbuf,nsr); }

  /* Say one last thing */
  debugline(RootProc,"Finished %5.1f %% of the simulation",100*curperc);

  /* Go home */
  return;
}

/* Close all the file streams */
void closeUniverse(void) {
  
  int i;
  
  /* Wait! */
  MPI_Barrier(Universe);

  /* Close each separate file stream [ONLY ON ROOT PROCESSOR] */
  if (Me == RootProc) {
    for (i=0; i<=Npoints.z; ++i) {
      fclose(FStreams[i]);
    }
  }

  /* Go home */
  return;
}

/********************
 ** FINAL THOUGHTS **
 ********************/

void finalize(void) {
  
  int n, nsum;
  double dtime, timesum;

  /* Note the time */
  gettimeofday(&TimeEnd, NULL);

  /* Time difference */
  dtime = (TimeEnd.tv_sec - TimeStart.tv_sec + (TimeEnd.tv_usec - TimeStart.tv_usec)/1e6);
  timesum = 0.0;
  MPI_Allreduce(&dtime,&timesum,1,MPI_DOUBLE,MPI_SUM,Universe);

  /* Collect number of steps from all processors */
  nsum = 0;
  MPI_Allreduce(&Ntotal,&nsum,1,MPI_INT,MPI_SUM,Universe);

  /* Print some miscelleneous information */
  debugline(RootProc,"Simulation run finished");
  debugline(RootProc,"Statistics:");
  n = (Npoints.x + 1) * (Npoints.y + 1) * (Npoints.z + 1);
  debugline(RootProc,"  Computed %d tip positions",n);
  debugline(RootProc,"  Needed %d minimization steps in total",nsum);
  debugline(RootProc,"  Which means approximately %.2f minimization steps per tip position",((double)nsum/n));
  debugline(RootProc,"  The simulation wall time is %.2f seconds",timesum);
  debugline(RootProc,"  The entire simulation took %.2f seconds",dtime);
  debugline(RootProc,"");
  
  /* Go home */
  return;
}

/***************************
 ** THE PARALLEL UNIVERSE **
 ***************************/

/* Initialize our parallel world */
void openParallelUniverse(int argc, char *argv[]) {
  
  int i;
  
  /* Start MPI */
  MPI_Init(&argc,&argv);
  
  /* Determine the size of the universe and which processor we are on */
  RootProc = 0;
  Universe = MPI_COMM_WORLD;
  MPI_Comm_rank(Universe,&Me);
  MPI_Comm_size(Universe,&NProcessors);
  
  /* Initialize the checker on how many x,y points for each processor */
  PointsOnProc = (int *)malloc(NProcessors*sizeof(int));
  for (i=0; i<NProcessors; ++i) { PointsOnProc[i] = 0; }

  /* Go home */
  return;
}

/* Terminate our parallel worlds */
void closeParallelUniverse(void) {
  
  int i;
  int *pop;
  
  /* How many x,y points on each processor */
  MPI_Barrier(Universe);
  pop = (int *)malloc(NProcessors*sizeof(int));
  for (i=0; i<NProcessors; ++i) { pop[i] = 0; }
  MPI_Allreduce(PointsOnProc,pop,NProcessors,MPI_INT,MPI_SUM,Universe);
  debugline(RootProc,"How many x,y points did each processor handle:");
  for (i=0; i<NProcessors; ++i) { debugline(RootProc,"  Processor %2d: %6d x,y points",i,pop[i]); }

  /* Close MPI */
  MPI_Finalize();

  /* Go home */
  return;
}
  
/**********************
 ** THE MAIN ROUTINE **
 **********************/

int main(int argc, char *argv[]) {
  
  /* Set up the parallel routines */
  openParallelUniverse(argc,argv);

  /* Initialize the simulation */
  parseCommandLine(argc,argv);  /* Read the command line */
  readInputFile();              /* Read input file */
  readXYZFile();                /* Read the XYZ file */
  readParameterFile();          /* Read the parameter file */

  /* The simulation itself */
  openUniverse();
  moveTip();
  closeUniverse();

  /* Some final thoughts */
  finalize();

  /* And stop the parallel routines properly */
  closeParallelUniverse();

  /* Done */
  return 0;
}
