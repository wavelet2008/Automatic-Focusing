// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: main script
******************************************************************************/

// main.cpp: This file contains the "main" function.
// This is where program execution begins and ends

#include "init.h"

#include "Header\operation_vector.h"

#include "Header\calculation_contrast.h"
#include "Header\calculation_histogram.h"

int main()
{
	cout << "Built with OpenCV " << CV_VERSION << endl;
	Mat img_bgr= imread("bar.jpg", 1);

	if (!img_bgr.data)  //or == if(src.empty())
	{
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

	//5-Area ROI center
	int center_ROI[2] = { int(height / 2) ,int(height / 2) };

	//5-Area ROI vector
	vector<int> ROI = VectorROI(img_gray, center_ROI);

	//gray level and their frequency
	vector<int> gray_level = VectorGrayLevel(1);
	vector<double> gray_frequency = VectorGrayLevelFrequency(ROI);

	//calculate avearge gray level
	double L_average = VectorMultiplication(gray_level, gray_frequency);

	//calculate index of gray value who is smaller or bigger than threshold
	vector<int> index_vector_below_average = VectorIndexBelowThreshold(gray_level, L_average);
	vector<int> index_vector_above_average = VectorIndexAboveThreshold(gray_level, L_average);
	
	//divide gray level
	vector<int> gray_level_below_average = VectorFromIndex(gray_level, index_vector_below_average);
	vector<int> gray_level_above_average = VectorFromIndex(gray_level, index_vector_above_average);

	//divide gray level frequency
	vector<double> gray_frequency_below_average = VectorFromIndex(gray_frequency, index_vector_below_average);
	vector<double> gray_frequency_above_average = VectorFromIndex(gray_frequency, index_vector_above_average);

	//cout << VectorSum(gray_frequency_below_average) << endl;
	//cout << VectorSum(gray_frequency_above_average) << endl;
	//cout << VectorSum(gray_frequency) << endl;

	//above average stands for foreground
	double L_above_average = VectorMultiplication(gray_level_above_average, gray_frequency_above_average) / VectorSum(gray_frequency_above_average);

	//below average stands for foreground
	double L_below_average = VectorMultiplication(gray_level_below_average, gray_frequency_below_average) / VectorSum(gray_frequency_below_average);

	//cout << L_above_average << endl;
	//cout << L_below_average << endl;

	//cout << VectorAverage(gray_level_above_average) << endl;
	//cout << VectorAverage(gray_level_below_average) << endl;

	double contrast = ContrastCenter(img_gray, "Michelson");
	//double contrast = CalculateContrast(ROI, "Whittle");
	//double contrast = CalculateContrast(ROI_A, "SD");

	cout << contrast << endl;

	//delete corresponds to new and delete[] corresponds to new[]
	//delete and delete[] play the same role in built-in data structure (pointer variable)
}
