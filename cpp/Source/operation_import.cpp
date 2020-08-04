// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Source-Operation on Import
******************************************************************************/

#include "..\Header\operation_import.h"
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
	if ("" == str) return res;
	//先将要切割的字符串从string类型转换为char*类型
	char* strs = new char[str.length() + 1]; //不要忘了
	strcpy(strs, str.c_str());

	char* d = new char[delim.length() + 1];
	strcpy(d, delim.c_str());

	char* p = strtok(strs, d);
	while (p) {
		string s = p; //分割得到的字符串转换为string类型
		res.push_back(s); //存入结果数组
		p = strtok(NULL, d);
	}

	return res;
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
Get bgr image matrix and construct a vector

Args:
	folder_path: folder path of images

Returns:
	rgb image series
*/
vector<Mat> VectorImgBGR(string& folder_path) {

	//vector of input image path
	vector<string> vector_files_path = VectorFilesPath(folder_path);

	//final result
	vector<Mat> vector_img_bgr;

	//generate matrix
	for (int k = 0; k < vector_files_path.size(); k++) {

		Mat that_img_bgr = imread(vector_files_path[k], 1);

		if (!that_img_bgr.data) {

			cout << "Could not open or find the image" << endl;
		}
		else {

			vector_img_bgr.push_back(that_img_bgr);
		}
	}
	return vector_img_bgr;
}
//------------------------------------------------------------------------------
/*
Get gray image matrix and construct a vector

Args:
	folder_path: folder path of images

Returns:
	gray image series
*/
vector<Mat> VectorImgGray(string& folder_path) {

	//vector of input image path
	vector<string> vector_files_path = VectorFilesPath(folder_path);

	//final result
	vector<Mat> vector_img_gray;

	//generate matrix
	for (int k = 0; k < vector_files_path.size(); k++) {

		cout << vector_files_path[k] << endl;

		vector<string> res = split(vector_files_path[k], "\\");
		/*for (int i = 0; i < res.size(); ++i)
		{
			cout << res[i] << endl;
		}*/
		cout << res[res.size()-1] << endl;

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

			vector_img_gray.push_back(that_img_gray);
		}
	}
	return vector_img_gray;
}