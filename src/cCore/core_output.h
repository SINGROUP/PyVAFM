#ifndef COREOUTPUT
#define COREOUTPUT


int Add_output( int owner, char* filename, int dump );
void output( circuit *c );
//int output_register (int, int, int);
//int output_register_feed(int outer, int feedid);
int output_close(int outer);
void output_printout( circuit *c ); //this is the function that prints stuff to file

#endif
