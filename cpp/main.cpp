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
#include "Header\calculation_articulation.h"
#include "Header\calculation_texture_feature.h"

int main()
{
	cout << "Built with OpenCV " << CV_VERSION << endl;
	Mat img_bgr = imread("campus.jpg", 1);

	if (!img_bgr.data) {

		cout << "Could not open or find the image" << endl;
		return -1;
	}

	//size of img
	int height = img_bgr.rows;
	int width = img_bgr.cols;

	//cout << height << endl;
	//cout << width << endl;

	//construct img gray//
	Mat img_gray(height, width, CV_8UC1);
	cvtColor(img_bgr, img_gray, CV_BGR2GRAY);

	//cout << Articulation(img_gray, "Variance") << endl;

	frame this_frame;
	this_frame.img_gray = img_gray;
	this_frame.img_bgr = img_bgr;

	//5-Area ROI center
	int center_ROI[2] = { int(height / 2) ,int(height / 2) };

	double contrast = ContrastCenter(this_frame, "Michelson");
	double articulation = Articulation(img_gray, "Laplacian");
	double contrast_texture=TextureFeatures(img_gray, "contrast");
	
	//string imgs_path = "C:\\Users\\魏华敬\\Desktop\\Experiment\\Luminance\\High\\Coarse";

	//vector<string> vector_imgs_path = VectorFilesPath(imgs_path);

	////VectorPrint(vector_imgs_path);

	//vector<Mat> vector_img_gray = VectorImgGray(imgs_path);

	//for (int k = 0; k < vector_img_gray.size(); k++) {

	//	double contrast = ContrastCenter(vector_img_gray[k], "Michelson");

	//	cout << contrast << endl;
	//}

	//slice vector
	//sort the image

	//delete corresponds to new and delete[] corresponds to new[]
	//delete and delete[] play the same role in built-in data structure (pointer variable)
}