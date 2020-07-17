# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 14:11:13 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title：initialization script
"""

import sys,os
    
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")+'\\Module'))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")+'\\Object'))
sys.path=list(set(sys.path)) 

import operation_path as O_P
import calculation_circle_array as C_A_A

from configuration_auto_focus_calibration import *