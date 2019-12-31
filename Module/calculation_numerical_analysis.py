# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 17:00:23 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title：Module-Numerical Calculation
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
            
        return [0.5]*len(which_list)
            
    else:
            
        return list((np.array(which_list)-minimum)/(maximum-minimum))