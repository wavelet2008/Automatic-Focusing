# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 17:00:27 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title：Module-Search of contrast peak value
"""

import numpy as np

#------------------------------------------------------------------------------
"""
Calculation of peak value in contrast value coarsely

Args:
    list_contrast: contrast value list
    list_VCM_code: VCM code list
    
Returns:
    start index and end index for fine search
"""
def FullSweepCoarse(list_contrast,list_VCM_code):
    
    #amount of consecutive ascending or descending points
    amount_revert=3
    
    amount_ascending=0
    amount_descending=0
    
    index_a=None
    index_b=None
        
    for k in range(len(list_contrast)-1):
        
        if list_contrast[k]<list_contrast[k+1]:
            
            amount_ascending+=1
            amount_descending=0
            
        if list_contrast[k]==list_contrast[k+1]:
        
            continue
            
        if list_contrast[k]>list_contrast[k+1]:
        
            amount_descending+=1
            amount_ascending=0

        #end index of ascending
        if amount_ascending>=amount_revert:
            
            index_a=k+1
            
        #start index of descending
        if amount_descending>=amount_revert:
            
            index_b=k-amount_descending
            
    #not void
    if index_a is None and index_b is None:
        
        index_a=list_contrast.index(np.max(list_contrast))-1
        index_b=list_contrast.index(np.max(list_contrast))+1
        
    return list_VCM_code[index_a],list_VCM_code[index_b]
 
#------------------------------------------------------------------------------
"""
Calculation of peak value in contrast value finely

Args:
    list_contrast: contrast value list
    list_VCM_code: VCM code list
    
Returns:
    VCM code of contrast peak value
"""   
def FullSweepFine(list_contrast,list_VCM_code):
    
    return list_VCM_code[list_contrast.index(np.max(list_contrast))]
    