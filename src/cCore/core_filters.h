#ifndef COREFILTERS
#define COREFILTERS

int Add_SKLP( int owner, double fcut, double Q, double gain );
void SKLP( circuit *c );
int Add_SKHP( int owner, double fcut, double Q, double gain );
void SKHP( circuit *c );
int Add_SKBP( int owner, double fcut, double band, double gain );
void SKBP( circuit *c );

int add_RCLP( int owner, double fcut, int order);
void RCLP( circuit *c );

int add_RCHP( int owner, double fcut, int order);
void RCHP( circuit *c );

#endif
