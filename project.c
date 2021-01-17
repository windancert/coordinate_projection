// laser_project_droplet.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main()
{
	cout << ("hello world\r\n");

	// # mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mzz, tx, ty, tz
	double mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mzz, tx, ty, tz;

	ifstream myfile;
	myfile.open("calibration_matrix.txt");

	myfile >> mxx >> myx >> mzx;
	myfile >> mxy >> myy >> mzy;
	myfile >> mxz >> myz >> mzz;
	myfile >> tx >> ty >> tz;

	myfile.close();

	
	double x = 90;
	double y = 90;
	double z = 22;

	double pixel_w = mzx * x + mzy * y + mzz * z + tz;
	double pixel_x = (mxx * x + mxy * y + mxz * z + tx) / -pixel_w;
	double pixel_y = (myx * x + myy * y + myz * z + ty) / -pixel_w;

	cout.precision(9);
	cout << pixel_x << endl;
	cout << pixel_y << "\r\n";

    return 0;
}

