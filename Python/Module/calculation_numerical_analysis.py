# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 17:00:23 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Numerical Calculation
"""

import numpy as np

#------------------------------------------------------------------------------
"""
Calculation of list normalization

Args:
    which_list: list to be operated
    
Returns:
    normalized list
"""
def Normalize(which_list):
    
    minimum=np.min(which_list)
    maximum=np.max(which_list)

    if minimum==maximum:
            
        return [0]*len(which_list)
            
    else:
            
        return list((np.array(which_list)-minimum)/(maximum-minimum))
    
#------------------------------------------------------------------------------
"""
List image matrix gray value of pixel in 8-neighbor

Args:
    img: image to be operated
    i,j: index of piexel
    
Returns:
    8-neighbor neighbor list
"""
def Neighbor(img,i,j):
    
    #image matrix index of pixel in 8-neighbor
    index_neighbor=[[i+diff_i,j+diff_j]for diff_i in [-1,0,1] for diff_j in [-1,0,1]]
    
    return [img[this_i,this_j] for this_i,this_j in index_neighbor if [this_i,this_j]!=[i,j]]
