# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 17:30:30 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title：Module-Experiment
"""

import matplotlib.pyplot as plt

from matplotlib.font_manager import FontProperties

import Path as Pa
import Contrast as Con

#annotation font
annotation_font=FontProperties(fname="C:\Windows\Fonts\GILI____.ttf",size=16)

#------------------------------------------------------------------------------
"""
Experiment: block module size factor

Args:
    imgs_folder: images folder  
    output_folder: figs output_folder
    both_series: if False: only Constant, if True: both Constant and Standard Deviation

Returns:
    None
"""
def ExperimentBlockModuleRatio(imgs_folder,output_folder,both_series=False):
    
    final_folder=output_folder+'\\Block Module\\Ratio\\'
    
    #construct a folder
    Pa.GenerateFolder(final_folder)   
    
    #ratio 0.1-0.9 step is 0.1
    for k in range(1,10):
        
        this_ratio=0.1*k
        
        '''Constant'''
        #plot curve
        Con.ContrastCurve(imgs_folder,'Constant','Block Module',ratio=this_ratio)

        plt.savefig(final_folder+str(k)+' (Constant).png')
        plt.close()
        
        if both_series:
            
            '''Standard Deviation'''
            #plot curve
            Con.ContrastCurve(imgs_folder,'Standard Deviation','Block Module',ratio=this_ratio)
        
            plt.savefig(final_folder+str(k)+' (Standard Deviation).png')
            plt.close()
        
#------------------------------------------------------------------------------
"""
Experiment: weight in 5 area method

Args:
    imgs_folder: images folder  
    output_folder: figs output_folder
    both_series: if False: only Constant, if True: both Constant and Standard Deviation

Returns:
    None
"""
def Experiment5AreaWeight(imgs_folder,output_folder,both_series=False):
    
    final_folder=output_folder+'\\5-Area\\Weight\\'
    
    #construct a folder
    Pa.GenerateFolder(final_folder)   
    
    #ratio 0.1-0.9 step is 0.1
    for k in range(1,10):
        
        center_weight=0.16+0.04*k
        
        this_weight=[center_weight]+4*[(1-center_weight)/4]
        
#        print(this_weight)
        
        '''Constant'''
        #plot curve
        Con.ContrastCurve(imgs_folder,'Constant','5-Area',weight=this_weight)
    
        plt.savefig(final_folder+str(k)+' (Constant).png')
        plt.close()
        
        if both_series:
            
            '''Standard Deviation'''
            #plot curve
            Con.ContrastCurve(imgs_folder,'Standard Deviation','5-Area',weight=this_weight)
        
            plt.savefig(final_folder+str(k)+' (Standard Deviation).png')
            plt.close()
        
#------------------------------------------------------------------------------
"""
Experiment: 5 area module factor

Args:
    imgs_folder: images folder  
    output_folder: figs output_folder
    both_series: if False: only Constant, if True: both Constant and Standard Deviation

Returns:
    None
"""
def Experiment5AreaFactor(imgs_folder,output_folder,both_series=False):
    
    final_folder=output_folder+'\\5-Area\\Factor\\'
    
    #construct a folder
    Pa.GenerateFolder(final_folder)   
    
    #ratio 0.1-0.9 step is 0.1
    for k in range(1,10):
         
        this_factor=10+2*k
        
#        print(this_weight)
        
        '''Constant'''
        #plot curve
        Con.ContrastCurve(imgs_folder,'Constant','5-Area',factor=this_factor)
    
        plt.savefig(final_folder+str(k)+' (Constant).png')
        plt.close()
        
        if both_series:
            
            '''Standard Deviation'''
            #plot curve
            Con.ContrastCurve(imgs_folder,'Standard Deviation','5-Area',factor=this_factor)
        
            plt.savefig(final_folder+str(k)+' (Standard Deviation).png')
            plt.close()