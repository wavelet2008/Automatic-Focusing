# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 16:11:05 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Calculation of Evaluation
"""

from configuration_color import list_contrast_operator,\
                                list_tenengrad_operator,\
                                list_texture_feature_operator

import calculation_contrast as C_C
import calculation_tenengrad as C_T
import calculation_texture_feature as C_T_F

#------------------------------------------------------------------------------
"""
Calculation of focus value function with different operator

Args:
    img_gray: matrix of gray img
    contrast_operator: operator of contrast calculation
    
Returns:
    focus value
"""
def FocusValue(img_gray,operator):
    
    '''Contrast'''
    if operator in list_contrast_operator:
    
        return C_C.GlobalContrast(img_gray,operator)
    
    '''Tenengrad'''
    if operator in list_tenengrad_operator:
        
        return C_T.Tenengrad(img_gray,operator)
    
    '''Texture Feature'''
    if operator in list_texture_feature_operator:
        
        return C_T_F.MapTextureFeature(img_gray)[operator]