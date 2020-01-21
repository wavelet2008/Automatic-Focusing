// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Header-operation on array
******************************************************************************/

#include "..\init.h"

#ifndef _OPERATION_VECTOR_H_
#define _OPERATION_VECTOR_H_

//Calculate sum of vector
int VectorSum(vector<int> which_vector);
float VectorSum(vector<float> which_vector);
double VectorSum(vector<double> which_vector);

//Calculate average of vector
double VectorAverage(vector<int> which_vector);
double VectorAverage(vector<float> which_vector);
double VectorAverage(vector<double> which_vector);

//Calculate maximum in an vector
int VectorMaximum(vector<int> which_vector);
double VectorMaximum(vector<double> which_vector);

//Calculate minimum in an vector
int VectorMinimum(vector<int> which_vector);
double VectorMinimum(vector<double> which_vector);

//The vector elements are multiplied
int VectorMultiplication(vector<int> vector_A, vector<int> vector_B);
double VectorMultiplication(vector<double> vector_A, vector<double> vector_B);
double VectorMultiplication(vector<int> vector_A, vector<double> vector_B);
double VectorMultiplication(vector<double> vector_A, vector<int> vector_B);

//vector of index of value which is bigger than threshold which_vector
vector<int> VectorIndexAboveThreshold(int* which_array, double threshold);
vector<int> VectorIndexAboveThreshold(vector<int> which_array, double threshold);

//list of index of value which is smaller than threshold which_array
vector<int> VectorIndexBelowThreshold(int* which_array, double threshold);
vector<int> VectorIndexBelowThreshold(vector<int> which_array, double threshold);

//Gets the new vector based on the index list
vector<int> VectorFromIndex(vector<int> which_vector, vector<int> index_vector);
vector<double> VectorFromIndex(vector<double> which_vector, vector<int> index_vector);

#endif