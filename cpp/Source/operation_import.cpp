// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Source-Operation on Import
******************************************************************************/

#include "..\Header\object_frame.h"
#include "..\Header\operation_import.h"
#include "..\Header\operation_vector.h"
#include "..\Header\calculation_contrast.h"

//------------------------------------------------------------------------------
/*
Split string like python does

Args:
	str: original string
	delim: separator string

Returns:
	separated string vector
*/
vector<string> split(const string& str, const string& delim) {

	vector<string> res;

	if ("" == str) {
		return res;
	}

	//the string to be cut is converted from string to char*
	char* strs = new char[str.length() + 1]; 
	strcpy(strs, str.c_str());

	char* d = new char[delim.length() + 1];
	strcpy(d, delim.c_str());

	char* p = strtok(strs, d);
	while (p) {

		//the split string is converted to string
		string s = p; 

		//put into the result array
		res.push_back(s); 
		p = strtok(NULL, d);
	}

	return res;
}
//Transfrom image path to VCM Code
int ImagePath2VCMCode(const string& image_name) {

	//split str into a vector
	vector<string> vector_str = split(image_name, "\\");
	string str_image = vector_str[vector_str.size() - 1];

	//str with .jpg or .png
	vector<string> vector_str_image = split(str_image, "_");
	string str_code_image = vector_str_image[vector_str_image.size() - 1];

	//true code str
	vector<string> vector_str_code = split(str_code_image, ".");
	string str_code = vector_str_code[0];

	//transfrom str to int
	return atoi(str_code.c_str());
}
int VectorIndex(vector<int>which_vector, int which_element) {

	for (int k = 0; k < which_vector.size(); k++) {
		
		if (which_vector[k] == which_element) {

			return k;
		}
	}
}
//------------------------------------------------------------------------------
/*
Calculate the path of all the files under the path

Args:
	folder_path: folder path of images

Returns:
	image files
*/
vector<string> VectorFilesPath(string& folder_path) {

	//final result
	vector<string> total_files;

	//File handle for later lookup
	intptr_t hFile = 0;

	//document information
	struct _finddata_t fileinfo;

	//temporary variable
	string path;

	//the first file is found
	if ((hFile = _findfirst(path.assign(folder_path).append("\\*").c_str(), &fileinfo)) != -1) {

		do {
			//condition: folder
			if ((fileinfo.attrib & _A_SUBDIR)) {

				if (strcmp(fileinfo.name, ".") != 0 && strcmp(fileinfo.name, "..") != 0) {

					//files which are from branch folder
					vector<string> branch_files = VectorFilesPath(path.assign(folder_path).append("\\").append(fileinfo.name));

					//collect them
					for (int k = 0; k < branch_files.size(); k++) {

						total_files.push_back(branch_files[k]);
					}
				}
			}
			//condition: file
			else {

				total_files.push_back(path.assign(folder_path).append("\\").append(fileinfo.name));
			}
		}
		//able to find other files
		while (_findnext(hFile, &fileinfo) == 0);

		//end the lookup and close the handle
		_findclose(hFile);
	}
	return total_files;
}
//------------------------------------------------------------------------------
/*
Get frame object and construct a vector

Args:
	folder_path: folder path of images

Returns:
	frame object series
*/
vector<frame> VectorFrame(string& folder_path) {

	//vector of input image path
	vector<string> vector_files_path = VectorFilesPath(folder_path);

	//vector if frame and VCM Code
	vector<frame> vector_frame;
	vector<int> vector_VCM_Code;

	//generate matrix
	for (int k = 0; k < vector_files_path.size(); k++) {

		//cout << vector_files_path[k] << endl;
	
		Mat that_img_bgr = imread(vector_files_path[k], 1);

		if (!that_img_bgr.data) {

			cout << "Could not open or find the image" << endl;
		}
		else {

			//size of img
			int height = that_img_bgr.rows;
			int width = that_img_bgr.cols;

			//construct img gray//
			Mat that_img_gray(height, width, CV_8UC1);
			cvtColor(that_img_bgr, that_img_gray, CV_BGR2GRAY);

			//generate a frame object
			frame this_frame;

			this_frame.img_gray = that_img_gray;
			this_frame.img_bgr = that_img_bgr;
			this_frame.VCM_Code = ImagePath2VCMCode(vector_files_path[k]);
			this_frame.contrast= ContrastCenter(this_frame, "Boccignone");

			vector_frame.push_back(this_frame);
			vector_VCM_Code.push_back(this_frame.VCM_Code);
		}
	}
	//copy the VCM Code vector
	vector<int> original_vector_VCM_Code= vector_VCM_Code;
	vector<int> vector_index_sorted;

	//sort the VCM Code
	sort(vector_VCM_Code.begin(), vector_VCM_Code.end());

	for (int i = 0; i < vector_VCM_Code.size(); i++) {

		vector_index_sorted.push_back(VectorIndex(original_vector_VCM_Code, vector_VCM_Code[i]));
	}
	return VectorFromIndex(vector_frame, vector_index_sorted);
}