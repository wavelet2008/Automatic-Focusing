# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 18:03:19 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title：Object-frame
"""

import cv2
import numpy as np

import calculation_contrast as C_C
from calculation_contrast import zoom_factor,ROI_weight

#==============================================================================
#object to operate image
#============================================================================== 
class frame:
    def __init__(self,
                 path=None,
                 pre_fix=None,
                 img_bgr=None,
                 img_gray=None,
                 img_ROI=None,
                 focus_value=None,
                 lens_position_code=None):
        self.path=path
        self.pre_fix=pre_fix
        self.img_bgr=img_bgr
        self.img_gray=img_gray
        self.img_ROI=img_ROI
        self.focus_value=focus_value
        self.lens_position_code=lens_position_code
        
    def Init(self,operator,ROI_mode):
        
        #read image
        self.img_bgr=cv2.imread(self.path)
        
        #convert rgb img to gray img
        self.img_gray=cv2.cvtColor(self.img_bgr,cv2.COLOR_BGR2GRAY)
        
        #VCM code calculation
        try:
            
            self.lens_position_code=int(self.path.strip('.jpg').split(self.pre_fix)[-1])
            
        except:
            
            self.lens_position_code=int(self.path.strip('.png').split(self.pre_fix)[-1])
            
        #size of img
        height,width=np.shape(self.img_gray)

        ROI_linewidth=int(height//300)
        
        #image of ROI
        self.img_ROI=np.full(np.shape(self.img_gray),np.nan)
        
        list_5_points=[[ height/2, width/2],
                       [ height/4, width/4],
                       [ height/4,-width/4],
                       [-height/4,-width/4],
                       [-height/4, width/4]]
        
        #size of area
        area_half_height=int(np.shape(self.img_gray)[0]/zoom_factor)
        area_half_width=int(np.shape(self.img_gray)[1]/zoom_factor)
            
        #calculate contrast in each area
        list_contrast_5_areas=[]
        
        if ROI_mode=='5-Area':
            
            for i,j in list_5_points:
                        
                this_area=self.img_gray[int(i)-area_half_height:int(i)+area_half_height,
                                        int(j)-area_half_width:int(j)+area_half_width]
            
                #collect it
                list_contrast_5_areas.append(C_C.GlobalContrast(this_area,operator))
            
                #draw the bound of ROI
                for k in range(ROI_linewidth):
                    
                    self.img_ROI[int(i-k)-area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                    self.img_ROI[int(i+k)+area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                    self.img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j-k)-area_half_width]=1
                    self.img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j+k)+area_half_width]=1
            
            #collect the data
            self.focus_value=np.sum(np.array(ROI_weight)*np.array(list_contrast_5_areas))
       
        if ROI_mode=='Center':
            
            for i,j in list_5_points[:1]:
                        
                this_area=self.img_gray[int(i)-area_half_height:int(i)+area_half_height,
                                        int(j)-area_half_width:int(j)+area_half_width]
            
                #collect it
                list_contrast_5_areas.append(C_C.GlobalContrast(this_area,operator))
            
                #draw the bound of ROI
                for k in range(ROI_linewidth):
                    
                    self.img_ROI[int(i-k)-area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                    self.img_ROI[int(i+k)+area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                    self.img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j-k)-area_half_width]=1
                    self.img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j+k)+area_half_width]=1
    
            #collect the data
            self.focus_value=list_contrast_5_areas[0]
            
        print('--> Lens Position Code:',self.lens_position_code)
        # print('--> Focus Value:',self.focus_value)