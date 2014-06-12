
//global list of circuits




/*
int init = 0;
size_t csize = sizeof(circuit);
size_t dsize = sizeof(double);
size_t isize = sizeof(int);

//int GlobalChannelCounter = 0;
//int GlobalCircuitCounter = 0;


//array containing all signals I and O
//double *GlobalSignals; 


int GlobalNFunctions = 4;
void (**ufunctions)(circuit*); //update functions
void (**ifunctions)(circuit*); //init functions
char **pynames; //python names for the circuits









void UpdateCircuit(circuit *c, void (*f)(circuit*)){

  f(c);

}
void Update(void){
  
  
  for(int i=0; i<GlobalCircuitCounter; i++){
    
    functions[circuits[i].ufunction]( &circuits[i] );

  }
  
}




// creates a list of all circuit functions
void Init(){
  
  GlobalNFunctions = 4; //correct this!
  ifunctions = (void**)malloc(GlobalNFunctions*sizeof(void*));
  ufunctions = (void**)malloc(GlobalNFunctions*sizeof(void*));
  pynames = (char**)malloc(GlobalNFunctions*sizeof(char*));

  int i=0;
  pynames[i] = "opADD"; ufunctions[i] = opADD; i++;
  pynames[i] = "opSUB"; ufunctions[i] = opSUB; i++;
  pynames[i] = "opMUL"; ufunctions[i] = opMUL; i++;
  pynames[i] = "opDIV"; ufunctions[i] = opDIV; i++;
}
*/
