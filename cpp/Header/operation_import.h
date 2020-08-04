// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Header-Operation on Import
******************************************************************************/

#include "..\init.h"

#ifndef _OPERATION_IMPORT_H_
#define _OPERATION_IMPORT_H_

//Split string like python does
vector<string> Split(const string& str, const string& delim);

//Transfrom image path to VCM Code
int ImagePath2VCMCode(const string& image_name);

//Calculate the path of all the files under the path
vector<string> VectorFilesPath(string& folder_path);

//Get gray image matrix and construct a vector
vector<frame> VectorFrame(string& folder_path);

#endif