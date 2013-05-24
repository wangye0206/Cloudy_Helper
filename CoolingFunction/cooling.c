#include "stdio.h"
#include "math.h"

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

/* Calculate Cooling Function */
float CoolingFunction(float T, float n, float Z)
{

	float Lambda;

	/* Eq 6 of Wang et al. 2013 */
	float lh_a = 4.86567e-13;
	float lh_b = -2.21974;
	float lh_c = 1.35332e-5;
	float lh_d = 9.64775;
	float lh_e = 1.11401e-9;
	float lh_f = -2.66528;
	float lh_g = 6.91908e-21;
	float lh_h = -0.571255;
	float lh_i = 2.45595e-27;
	float lh_j = 0.49521;

	float Lambda_h = (lh_a * pow(T,lh_b) + pow(lh_c * T,lh_d)*(lh_e * pow(T,lh_f) + lh_g * pow(T,lh_h))) / (1 + pow(lh_c * T, lh_d)) + lh_i * pow(T,lh_j);

	//printf("Lambda_h is %e\n", Lambda_h);

	/* Eq 7 of Wang et al. 2013 */
	float dh_a = 2.84738;
	float dh_b = 3.62655e13;
	float dh_g1 = -3.18564e-4;
	float dh_g2 = 4.8323e-3;
	float dh_g3 = -0.0225974;
	float dh_g4 = 0.0245446;

	float dh_g = dh_g1 * pow(n,4) + dh_g2 * pow(n,3) + dh_g3 * pow(n,2) + dh_g4 * n + 1;
	
	float D_h = ( pow(T,dh_a) + dh_b * dh_g )/( pow(T,dh_a) + dh_b );

	//printf("D_h is %e\n", D_h);

	/* Eq 9 of Wang et al. 2013 */
	float lm_a = 6.88502e30;
	float lm_b = -1.90262;
	float lm_c = 2.48881e17;
	float lm_d = 0.771176;
	float lm_e = 3.00028e-28;
	float lm_f = 0.472682;

	float Lambda_m = Z * (lm_e * pow(T,lm_f) + pow((lm_a * pow(T, lm_b) + lm_c * pow(T, lm_d)), -1));

	//printf("Lambda_m is %e\n", Lambda_m);

	/* Eq 10 of Wang et al. 2013 */
	float dm_a = 3.29383;
	float dm_b = 8.82636e14;
	float dm_g1 = 0.00221438;
	float dm_g2 = -0.0353337;
	float dm_g3 = 0.0524811;
	
	float D_m = ( pow(T,dm_a) + dm_b * (dm_g1 * pow(n,3) + dm_g2 * pow(n,2) + dm_g3 * n + 1) )/( pow(T,dm_a) + dm_b );

	//printf("D_m is %e\n", D_m);

	/* Eq 11 of Wang et al. 2013 */
	float Lambda_e = ((HIGH_T_ELECTRON_FRACTION * FINE_STRUCTURE_CONSTANT * THOMSON_CROSS_SECTION * pow(BOLTZMANN_CONSTANT,2))/(ELECTRON_MASS * LIGHT_SPEED)) * 2.63323 * pow(T,1.708064);

	//printf("Lambda_e is %e\n", Lambda_e);
	
	float me_a = 0.00769985;

	/* High Temperature Approximation of Eq 14 of Wang et al. 2013 */
	float M_e = me_a * (Z - 1) + 1;

	//printf("M_e is %e\n", M_e);

	Lambda = D_h * Lambda_h +  D_m * Lambda_m + M_e * Lambda_e;

	return Lambda;
}

float CoolingRate(float T, float n, float Z)
{
	float rate;
	float Lambda = CoolingFunction(T, n, Z);

	/* Election fraction, Eq 12 of Wang et al. 2013 */
	float E = 2.1792 - exp(3966.27/T);
	float a = 0.00769985;
	float b = 24683.1;
	float c = 0.805234;

	/* Eq 14 of Wang et al. 2013 */
	float M = ((a * Z - a + 1) * pow(T,c) + b)/(pow(T,c) + b);

	//printf("E is %f, M is %f\n",E,M);

	rate = E * M * pow(pow(10,n),2) * Lambda;

	return rate;
}

/* This is a example to show how to use CoolingFunction and CoolingRate */

int main()
{
	/* Temperature, K */
	float temperature = 1e7;

	/* Hydrogen Density log10(n_H) */
	float density = 10;

	/* Metallicity, Z_sun */
	float metallicity = 15;

	/* Cooling Function, erg s-1 cm3 */
	float Lambda = CoolingFunction(temperature, density, metallicity);

	/* Cooling Rate, erg s-1 cm-3 */
	float L = CoolingRate(temperature, density, metallicity);

	printf("T = %f, n = %f, Z = %f, Lambda = %e, L = %e\n", temperature, density, metallicity, Lambda, L);
	
	return 0;
}
