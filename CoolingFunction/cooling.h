#ifndef COOLING_H_
#define COOLING_H_

/* Replace these constants with yours, if you have difined them in your code */

/* Thomson cross-section, cm^2 */
const float THOMSON_CROSS_SECTION = 6.65e-25;

/* light speed, cm/s */
const float LIGHT_SPEED = 2.99792458e10;

/* fine structure constant */
const float FINE_STRUCTURE_CONSTANT = 7.2973525698e-3;

/* boltzmann constant, erg/K */
const float BOLTZMANN_CONSTANT = 1.3806488e-16;

/* electron mass, gram */
const float ELECTRON_MASS = 9.10938291e-28;

/* electron density/hydrogen density at solar abudance and
 * fully ionized status, value here derived with abundance
 * GASS discribed in CLOUDY */
const float HIGH_T_ELECTRON_FRACTION = 1.1972;

float CoolingFunction(float T, float n, float Z);

float CoolingRate(float T, float n, float Z);

#endif
