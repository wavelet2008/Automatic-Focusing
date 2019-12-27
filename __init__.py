# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 16:17:21 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title：initialization script
"""

import sys,os
    
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'\\Module')
#sys.path.append(os.getcwd()+'\\Object')
sys.path=list(set(sys.path))

import Path as Pa
import Import as Im
import Contrast as Con
import Histogram as Hist
import Experiment as Exp
import Discrimination as Dis