# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 17:30:30 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title：Module-Experiment
"""

import os
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
            
#------------------------------------------------------------------------------
"""
Operate comparison experiment

Args:
    folder_experiment: experiment imgs total folder
    save_fig: whether to save fog (default: True)
    
Returns:
    None
"""
def ExperimentComparison(folder_experiment,save_fig=True):
    
    for name_this_group in os.listdir(folder_experiment):
        
        #join the path
        folder_this_group=folder_experiment+'\\'+name_this_group
        
    #    print(folder_this_group)
        
        #imgs of this group experiment
        list_imgs_folder=[]
        
        for name_this_imgs_folder in os.listdir(folder_this_group):
        
            if '.png' in name_this_imgs_folder:
                
                continue
            
            #join the path
            this_imgs_folder=folder_this_group+'\\'+name_this_imgs_folder
            
    #        print(this_imgs_folder)
            
            list_imgs_folder.append(this_imgs_folder)
            
        #Constant contrast mode
        Con.ContrastCurve(list_imgs_folder,'Constant')
        
        if save_fig:
            
            plt.savefig(folder_this_group+'\\Constant.png')
            plt.close()
        
        #Advanced contrast mode
        Con.ContrastCurve(list_imgs_folder,'Advanced')
        
        if save_fig:
            
            plt.savefig(folder_this_group+'\\Advanced.png')
            plt.close()
            
        #Standard Deviation contrast mode
        Con.ContrastCurve(list_imgs_folder,'Standard Deviation')
        
        if save_fig:
            
            plt.savefig(folder_this_group+'\\Standard Deviation.png')
            plt.close()