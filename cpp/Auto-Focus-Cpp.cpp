// Auto-Focus-Cpp.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <stdio.h>
#include <tchar.h>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2\imgproc\imgproc.hpp>
#include <opencv2\imgproc\imgproc_c.h>
#include <opencv2\highgui\highgui.hpp>

using namespace cv;
using namespace std;

//Calculate length of array
//overloaded function 1: pointer array of int type
int ArrayLength(int* which_array) {

	int length = _msize(which_array) / sizeof(which_array[0]);

	return length;
}
//overloaded function 2: pointer array of float type
int ArrayLength(float* which_array) {

	int length = _msize(which_array) / sizeof(which_array[0]);

	return length;
}
//overloaded function 3: array pointer of double type
int ArrayLength(double* which_array) {

	int length = _msize(which_array) / sizeof(which_array[0]);

	return length;
}
//overloaded function 4: pointer array of char type
//char could be the pointer variable
int ArrayLength(char* which_array) {

	int length = _msize(which_array) / sizeof(which_array[0]);

	return length;
}

//Calculate sum of array
//overloaded function 1: pointer array of int type
int ArraySum(int* which_array) {

	//final result
	int sum = 0;

	for (int i = 0; i < ArrayLength(which_array); i++) {

		sum += which_array[i];
	}
	return sum;
}
//overloaded function 2: pointer array of float type
float ArraySum(float* which_array) {

	//final result
	float sum = 0;

	for (int i = 0; i < ArrayLength(which_array); i++) {

		sum += which_array[i];
	}
	return sum;
}
//overloaded function 3: pointer array of double type
double ArraySum(double* which_array) {

	//final result
	double sum = 0;

	for (int i = 0; i < ArrayLength(which_array); i++) {

		sum += which_array[i];
	}
	return sum;
}

//Calculate average of array
//overloaded function 1: pointer array of int type
double ArrayAverage(int* which_array) {

	int sum = ArraySum(which_array);

	return double(sum) / ArrayLength(which_array);
}
//overloaded function 1: pointer array of float type
double ArrayAverage(float* which_array) {

	float sum = ArraySum(which_array);

	return double(sum) / ArrayLength(which_array);
}
//overloaded function 1: pointer array of double type
double ArrayAverage(double* which_array) {

	double sum = ArraySum(which_array);

	return double(sum) / ArrayLength(which_array);
}

//The vector elements are multiplied
//overloaded function 1: both array of int
int VectorMultiplication(int* array_A, int* array_B) {

	//judge if the length is the same
	if (ArrayLength(array_A) == ArrayLength(array_B)) {

		//final result
		int sum = 0;

		for (int i = 0; i < ArrayLength(array_A); i++) {
		
			sum += array_A[i] * array_B[i];
		}
		return sum;
	}
	else {

		cout << "--> ERROR: Incorrct size of array";
		return 0;
	}
}
//overloaded function 2: array of int and float
float VectorMultiplication(int* array_A, float* array_B) {

	//judge if the length is the same
	if (ArrayLength(array_A) == ArrayLength(array_B)) {

		//final result
		float sum = 0;

		for (int i = 0; i < ArrayLength(array_A); i++) {

			sum += array_A[i] * array_B[i];
		}
		return sum;
	}
	else {

		cout << "--> ERROR: Incorrct size of array";
		return 0;
	}
}
//overloaded function 3: array of int and double
double VectorMultiplication(int* array_A, double* array_B) {

	//judge if the length is the same
	if (ArrayLength(array_A) == ArrayLength(array_B)) {

		//final result
		double sum = 0;

		for (int i = 0; i < ArrayLength(array_A); i++) {

			sum += array_A[i] * array_B[i];
		}
		return sum;
	}
	else {

		cout << "--> ERROR: Incorrct size of array";
		return 0;
	}
}

//list of index of value which is bigger than threshold which_array
int* ListIndexAboveThreshold(int* which_array, double threshold) {
	
	const int length = ArrayLength(which_array);
	
	//define a pointer array
	int* list_index = new int[length];

	//real length of array
	int real_length = 0;

	for (int i = 0; i < length; i++) {

		if (which_array[i] < threshold) {

			list_index[i] = i;
			real_length++;
		}
	}
	//cout << _msize(list_index) / sizeof(list_index[0]) << endl;

	//final result
	int* real_list_index = new int[real_length];

	for (int i = 0; i < real_length; i++) {

		real_list_index[i] = list_index[i];
	}
	//cout << _msize(real_list_index) / sizeof(real_list_index[0]) << endl;
	//cout << real_list_index[0] << endl;

	delete[]list_index;
	return real_list_index;
}

//list of index of value which is smaller than threshold which_array
int* ListIndexBelowThreshold(int* which_array, double threshold) {

	const int length = ArrayLength(which_array);

	//define a pointer array
	int* list_index = new int[length];

	//real length of array
	int real_length = 0;

	for (int i = 0; i < length; i++) {

		if (which_array[i] > threshold) {

			list_index[i] = i;
			real_length++;
		}
	}
	//cout << _msize(list_index) / sizeof(list_index[0]) << endl;

	//final result
	int* real_list_index = new int[real_length];

	for (int i = 0; i < real_length; i++) {

		real_list_index[i] = list_index[i];
	}
	//cout << _msize(real_list_index) / sizeof(real_list_index[0]) << endl;

	delete[]list_index;
	return real_list_index;
}
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

	//record the number of pixels at the gray level
	int amount[256] = { 0 };

	//the total number of pixels
	int area_img = height * width;

	//probability of the input image at each gray level
	double frequency[256] = { 0 };

	//matrix as an array
	int* array_img = new int[area_img];

	//get the number of pixels under each gray level is obtained
	for (int i = 0; i < height; i++)
	{
		for (int j = 0; j < width; j++)
		{
			int gray_value = img_gray.at<uchar>(i, j);

			//accumulate
			amount[gray_value]++;
			array_img[i * width + j] = gray_value;
		}
	}
	//the probability distribution of each gray level is obtained
	for (int i = 0; i < 256; i++) {

		frequency[i]= ((double)amount[i]) / area_img;
	}
	
	//convert to pointer variable
	int* gray_level= new int[256];
	double* gray_frequency = new double[256];

	for (int i = 0; i < 256; i++) {

		gray_level[i] = i;
		gray_frequency[i] = frequency[i];
	}

	//cout << ArrayLength(gray_level) << endl;
	//cout << ArrayLength(gray_frequency) << endl;

	//calculate avearge gray level
	double L_mean = VectorMultiplication(gray_level, gray_frequency);

	//cout << L_mean << endl;
	//cout << ArrayAverage(array_img) << endl;

	ListIndexAboveThreshold(gray_level, L_mean);
	int* list_index = ListIndexBelowThreshold(gray_level, L_mean);
	
	cout << list_index[0] << endl;;

	//delete corresponds to new and delete[] corresponds to new[]
	//delete and delete[] play the same role in built-in data structure (pointer variable)
	//delete[]gray_level;
	//delete[]gray_frequency;
}
