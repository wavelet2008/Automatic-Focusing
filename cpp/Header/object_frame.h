// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Header-frame object
******************************************************************************/

#include "..\init.h"

#ifndef _OBJECT_FRAME_H_
#define _OBJECT_FRAME_H_

//frame object
class frame {

public:
	int VCM_code;
	double offset;
	double contrast;
	Mat img_bgr;
	Mat img_gray;
	frame();
};
	
#endif