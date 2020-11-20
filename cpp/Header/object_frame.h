// -*- coding: utf-8 -*-
/******************************************************************************
Created on Mon Sept 11 14:51:37 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: wei@kamerawerk.cn

@title: Header-frame object
******************************************************************************/

#include "..\init.h"

#ifndef _OBJECT_FRAME_H_
#define _OBJECT_FRAME_H_

//frame object
class frame {

public:
	int lens_position_code;
	double object_distance;
	double focus_value;
	Mat img_bgr;
	Mat img_gray;
	frame();
};
	
#endif