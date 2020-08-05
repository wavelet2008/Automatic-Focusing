// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Script-main
******************************************************************************/

// main.cpp: This file contains the "main" function.
// This is where program execution begins and ends

#include "init.h"

#include "Header\object_frame.h"

#include "Header\operation_import.h"
#include "Header\operation_vector.h"

#include "Header\calculation_contrast.h"
#include "Header\calculation_histogram.h"
#include "Header\calculation_peak_search.h"
#include "Header\calculation_articulation.h"
#include "Header\calculation_texture_feature.h"

int main()
{
	cout << "Built with OpenCV " << CV_VERSION << endl;

	//string img_name = "campus.jpg";
	//Mat img_bgr = ReadImgBGR(img_name);

	string imgs_path = "C:\\Users\\ASUS\\Desktop\\Experiment\\Random\\Polight";

	vector<frame> vector_frame = VectorFrame(imgs_path);
	
	//vector of contrast
	vector<double> vector_contrast;

	for (int k = 0; k < vector_frame.size(); k++) {

		vector_contrast.push_back(vector_frame[k].contrast);
		
		if (FullSweepCoarse(vector_contrast) != -1) {

			break;
		}
	}
	cout << "" << endl;
	cout << "-- Fcoused VCM Code: " << vector_frame[FullSweepCoarse(vector_contrast)].VCM_Code << endl;

	//delete corresponds to new and delete[] corresponds to new[]
	//delete and delete[] play the same role in built-in data structure (pointer variable)
}