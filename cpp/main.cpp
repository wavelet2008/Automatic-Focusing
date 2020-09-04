// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: script-Automatic Focusing Simulation
******************************************************************************/

// main.cpp: This file contains the "main" function.
// This is where program execution begins and ends

#include "init.h"

#include "Header\object_frame.h"

#include "Header\operation_import.h"
#include "Header\operation_vector.h"

#include "Header\calculation_QR_code.h"
#include "Header\calculation_contrast.h"
#include "Header\calculation_histogram.h"
#include "Header\calculation_peak_search.h"
#include "Header\calculation_articulation.h"
#include "Header\calculation_texture_feature.h"
#include "Header\calculation_numerical_analysis.h"

int main(){

	cout << "Built with OpenCV " << CV_VERSION << endl;

	//Mat img_QR_code = ReadImgBGR("AF_QR_Code_Scanner.jpg");
	//ReadQRCode(img_QR_code, "zxing-cpp-master");

	string imgs_path = "C:\\Users\\ASUS\\Desktop\\Material\\poLight-Large-Fine\\300mm";

	vector<frame> vector_frame = VectorFrame(imgs_path);
	
	//vector of code and contrast
	vector<int> vector_code;
	vector<double> vector_contrast;

	for (int k = 0; k < vector_frame.size(); k++) {

		vector_code.push_back(vector_frame[k].lens_position_code);
		vector_contrast.push_back(vector_frame[k].focus_value);
	}

	cout << "" << endl;
	cout << "-- Fcoused Lens Position Code: " << vector_frame[FullSweepFine(vector_contrast)].lens_position_code << endl;

	//write VCM Code and contrast
	ofstream out_file;
	out_file.open("Code-Contrast.txt");
	out_file << "Code" << " " << "Contrast" << endl;

	//normalization
	vector<double> vector_normalized_contrast = Normalize(vector_contrast);

	for (int k = 0; k < vector_contrast.size(); k++) {

		out_file << vector_code[k] << " " << vector_normalized_contrast[k] << endl;
	}
	return 0;

	//delete corresponds to new and delete[] corresponds to new[]
	//delete and delete[] play the same role in built-in data structure (pointer variable)
}