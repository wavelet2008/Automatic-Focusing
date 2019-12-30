# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 18:03:19 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title：Object-frame
"""

import cv2

#==============================================================================
#object to operate image
#============================================================================== 
class frame:
    def __init__(self,
                 path=None,
                 pre_fix=None,
                 img_bgr=None,
                 img_gray=None,
                 VCM_code=None):
        self.path=path
        self.pre_fix=pre_fix
        self.img_bgr=img_bgr
        self.img_gray=img_gray
        self.VCM_code=VCM_code
   
    def Init(self):
        
        #read image
        self.img_bgr=cv2.imread(self.path)
        
        #convert rgb img to gray img
        self.img_gray=cv2.cvtColor(self.img_bgr,cv2.COLOR_BGR2GRAY)
        
        #VCM code calculation
        self.VCM_code=int(self.path.strip('.jpg').split(self.pre_fix)[-1])
        