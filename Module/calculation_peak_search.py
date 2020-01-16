# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 17:00:27 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title：Module-Search of contrast peak value
"""

import os
import copy as cp
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import MultipleLocator
from matplotlib.font_manager import FontProperties

import operation_path as O_P
import operation_import as O_I
import operation_dictionary as O_D

import calculation_contrast as C_C
import calculation_numerical_analysis as C_N_A

#font of fonts of all kinds
legend_prop={'family':'Gill Sans MT','weight':'normal','size':12}
text_font=FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=12)
label_font=FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=16)
title_font=FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=18)
sample_font=FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=12)

list_contrast_operator=['KK',
                        'Whittle',
                        'Burkhardt',
                        'Michelson',
                        'Peli',
                        'W3C',
                        'Weber',
                        'Stevens',
                        'Boccignone',
                        'SD',
                        'SDLG',
                        'SAM',
                        'SALGM',
                        'SAW',
                        'SALGW',
                        'RMSC-1',
                        'RMSC-2',
                        'Tadmor-1',
                        'Tadmor-2',
                        'Tadmor-3',
                        'Rizzi']
        
list_contrast_color=['tan',
                     'teal',
                     'olive',
                     'maroon',
                     'orchid',
                     'fuchsia',
                     'crimson',
                     'magenta',
                     'thistle',
                     'chocolate',
                     'firebrick',
                     'rosybrown',
                     'slategray',
                     'steelblue',
                     'slateblue',
                     'cadetblue',
                     'lightsalmon',
                     'mediumvioletred',
                     'mediumslateblue',
                     'mediumturquoise',
                     'mediumaquamarine']

#map between mode and color     
map_mode_color=dict(zip(list_contrast_operator,list_contrast_color))

#------------------------------------------------------------------------------
"""
Calculation of peak value in contrast value coarsely

Args:
    list_contrast: contrast value list
    
Returns:
    start index and end index for fine search
"""
def FullSweepCoarse(list_contrast):
  
    #amount of consecutive ascending or descending points
    amount_revert=5
    
    #real-time
    amount_ascending,amount_descending=0,0
    
    #strat and end point for fine search
    index_a,index_b=None,None
    
    #index of maximum
    index_maximum=list_contrast.index(np.max(list_contrast))
    
    '''try to tolerate one fluctuation'''
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
            
            index_b=k-amount_descending+1

    if index_a!=None and index_b!=None:
        
        #expire the exception
        if index_a==index_maximum or index_b==index_maximum:
            
            return index_a-1,index_b+1
    
    else:
        
        return
 
#------------------------------------------------------------------------------
"""
Calculation of peak value in contrast value finely

Args:
    list_contrast: contrast value list
    
Returns:
    index of VCM code of contrast peak value
"""   
def FullSweepFine(list_contrast):
    
    return list_contrast.index(np.max(list_contrast))

#------------------------------------------------------------------------------
"""
Plot input image as well as contrast curve

Args:
   imgs_folder: folder which contains a batch of images 
   contrast_operator: operator of contrast calculation 
   
Returns:
    None
"""
def FullSweep(imgs_folder,contrast_operator):
    
    print('')
    print('-- Full Sweep')
    print('-> Operator:',contrast_operator)
    
    str_a,str_b=imgs_folder.split('Experiment')
    str_c,str_d=imgs_folder.split('Experiment')[-1].strip('\\').split('\\')
    
    #construct output folder
    output_folder_operator=str_a+'\\Contrast\\Scenario'+str_b
    output_folder_condition=output_folder_operator.split(str_c)[0].replace('\\Scenario','')+'\\Operator'
    
    output_folder_operator+='\\'+contrast_operator+'\\'
    output_folder_condition+='\\'+contrast_operator+'\\'
    
    O_P.GenerateFolder(output_folder_operator)
    O_P.GenerateFolder(output_folder_condition)
    
    '''need optimized frames construction'''
    list_imgs_folder=[imgs_folder+'\\'+this_name for this_name in os.listdir(imgs_folder) if '.' not in this_name]

    #construct frame objects
    imgs_folder_coarse=''
    imgs_folder_fine=''
    
    for this_imgs_folder in list_imgs_folder:
        
        if 'Coarse' in this_imgs_folder:

            imgs_folder_coarse=cp.deepcopy(this_imgs_folder)
        
        if 'Fine' in this_imgs_folder:

            imgs_folder_fine=cp.deepcopy(this_imgs_folder)
    
    if imgs_folder_coarse=='' or imgs_folder_fine=='':
        
        print('--> ERROR: Incorrect images folder')
        
        return
    
    #frame object for coarse and fine search
    frames_coarse=O_I.FramesConstruction(imgs_folder_coarse)
    frames_fine=O_I.FramesConstruction(imgs_folder_fine)
    
    #total data of coarse frames
    list_VCM_code_coarse=[]
    list_contrast_coarse=[]
    list_img_ROI_coarse=[]

    if contrast_operator not in list_contrast_operator:
        
        return print('=> ERROR: Incorrect Input')

    result_full_sweep=None
    
    print('')
    print('-- Full Sweep Coarse')
    
    #traverse all frames for full sweeping
    for this_frame in frames_coarse:

        img_gray=this_frame.img_gray
           
        #size of img
        height,width=np.shape(img_gray)
        
        #basic parameters
        ROI_weight=[0.44,0.14,0.14,0.14,0.14]
        zoom_factor=18
        ROI_linewidth=int(height//300)
        text_position='Contrast'
        
    #    print(height,width)
        
        #image of ROI
        this_img_ROI=np.full(np.shape(img_gray),np.nan)
        
        list_5_points=[[ height/2, width/2],
                       [ height/4, width/4],
                       [ height/4,-width/4],
                       [-height/4,-width/4],
                       [-height/4, width/4]]
        
        #size of area
        area_half_height=int(np.shape(img_gray)[0]/zoom_factor)
        area_half_width=int(np.shape(img_gray)[1]/zoom_factor)
        
        #calculate contrast in each area
        list_contrast_5_areas=[]
        
        for i,j in list_5_points:
                    
            this_area=img_gray[int(i)-area_half_height:int(i)+area_half_height,
                               int(j)-area_half_width:int(j)+area_half_width]
        
            #collect it
            list_contrast_5_areas.append(C_C.GlobalContrast(this_area,contrast_operator))
        
            #draw the bound of ROI
            for k in range(ROI_linewidth):
                
                this_img_ROI[int(i-k)-area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                this_img_ROI[int(i+k)+area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                this_img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j-k)-area_half_width]=1
                this_img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j+k)+area_half_width]=1

        #collect the data
        list_VCM_code_coarse.append(this_frame.VCM_code)
        list_contrast_coarse.append(np.sum(np.array(ROI_weight)*np.array(list_contrast_5_areas)))
        list_img_ROI_coarse.append(this_img_ROI)
       
        #result of full sweep
        result_full_sweep=FullSweepCoarse(list_contrast_coarse)
        
        print('--> VCM Code:',this_frame.VCM_code)
        
        if result_full_sweep is not None:
            
            #index for fine search
            index_start,index_end=result_full_sweep
            
            break

    #no valid peak: select maximum instead
    if result_full_sweep is None:

        index_start=list_contrast_coarse.index(np.max(list_contrast_coarse))-1
        index_end=list_contrast_coarse.index(np.max(list_contrast_coarse))+1
      
    #expetion    
    if index_start<0:
        
        index_start=0
        
    if index_end>=len(list_contrast_coarse):
        
        index_end=len(list_contrast_coarse)-1
    
    #VCM code boundary for fine search
    VCM_code_start=list_VCM_code_coarse[index_start]
    VCM_code_end=list_VCM_code_coarse[index_end]
    
    #frame list for final search
    frames=[]
    
    for this_frame in frames_fine:
        
        if VCM_code_start<=this_frame.VCM_code<=VCM_code_end:
            
            frames.append(this_frame)

    #if blank
    if frames==[]:

        flag='Coarse'

        list_VCM_code_fine=[]
        list_contrast_fine=[]
        
    else:
        
        flag='Fine'
   
        #total data of fine frames
        list_VCM_code_fine=[]
        list_contrast_fine=[]
        list_img_ROI_fine=[]
        
        print('')
        print('-- Full Sweep Fine')
        
        #traverse all frames for full sweeping
        for this_frame in frames:
    
            img_gray=this_frame.img_gray
               
            #size of img
            height,width=np.shape(img_gray)
            
            #basic parameters
            ROI_weight=[0.44,0.14,0.14,0.14,0.14]
            zoom_factor=18
            ROI_linewidth=int(height//300)
            text_position='Contrast'
            
        #    print(height,width)
            
            #image of ROI
            this_img_ROI=np.full(np.shape(img_gray),np.nan)
            
            list_5_points=[[ height/2, width/2],
                           [ height/4, width/4],
                           [ height/4,-width/4],
                           [-height/4,-width/4],
                           [-height/4, width/4]]
            
            #size of area
            area_half_height=int(np.shape(img_gray)[0]/zoom_factor)
            area_half_width=int(np.shape(img_gray)[1]/zoom_factor)
            
            #calculate contrast in each area
            list_contrast_5_areas=[]
            
            for i,j in list_5_points:
                        
                this_area=img_gray[int(i)-area_half_height:int(i)+area_half_height,
                                   int(j)-area_half_width:int(j)+area_half_width]
            
                #collect it
                list_contrast_5_areas.append(C_C.GlobalContrast(this_area,contrast_operator))
            
                #draw the bound of ROI
                for k in range(ROI_linewidth):
                    
                    this_img_ROI[int(i-k)-area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                    this_img_ROI[int(i+k)+area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                    this_img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j-k)-area_half_width]=1
                    this_img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j+k)+area_half_width]=1
    
            #collect the data
            list_VCM_code_fine.append(this_frame.VCM_code)
            list_contrast_fine.append(np.sum(np.array(ROI_weight)*np.array(list_contrast_5_areas)))
            list_img_ROI_fine.append(this_img_ROI)
           
            print('--> VCM Code:',this_frame.VCM_code)

    '''combine coarse and fine frames'''
    list_VCM_code=list_VCM_code_coarse+list_VCM_code_fine
    list_contrast=list_contrast_coarse+list_contrast_fine
    
    #construct map between VCM code and contrast
    map_VCM_code_frames=dict(zip(list_VCM_code,list_contrast))
    
    #sort the VCM code list in an ascending order
    list_VCM_code=list(set(list_VCM_code))
    list_VCM_code.sort()
    
    list_contrast=list(O_D.DictSortByIndex(map_VCM_code_frames,list_VCM_code).values())   
    
    #normalization of contrast list
    list_normalized_contrast=C_N_A.Normalize(list_contrast)

    plt.figure(figsize=(17,6))
    
    '''input image and bound'''
    ax_input_image=plt.subplot(121)
    
    '''AF result: peak VCM code'''  
    if flag=='Coarse':

        peak_index=FullSweepFine(list_contrast_coarse)
        peak_VCM_code=list_VCM_code_coarse[peak_index]
        peak_normalized_contrast=C_N_A.Normalize(list_contrast_coarse)[peak_index]
        
        plt.imshow(frames_coarse[peak_index].img_gray,cmap='gray')
        plt.imshow(list_img_ROI_coarse[peak_index],cmap='seismic_r')
         
    if flag=='Fine':

        peak_index=FullSweepFine(list_contrast_fine)
        peak_VCM_code=list_VCM_code_fine[peak_index]
        peak_normalized_contrast=C_N_A.Normalize(list_contrast_fine)[peak_index]
        
        plt.imshow(frames[peak_index].img_gray,cmap='gray')
        plt.imshow(list_img_ROI_fine[peak_index],cmap='seismic_r') 
        
    print('--> Peak VCM Code:',peak_VCM_code)
    
    #center of ROI
    list_5_center_ROI=[[  height/2,   width/2],
                       [  height/4,   width/4],
                       [  height/4, 3*width/4],
                       [3*height/4, 3*width/4],
                       [3*height/4,   width/4]]
    
    if text_position=='Image':
    
        #show ROI weight
        for kk in range(len(list_5_center_ROI)):
            
            #center coordinates of ROI
            y_center_ROI=list_5_center_ROI[kk][0]+height/60
            x_center_ROI=list_5_center_ROI[kk][1]-width/40
            
            ax_input_image.text(x_center_ROI,
                                y_center_ROI,
                                '%.2f'%(ROI_weight[kk]),
                                fontproperties=text_font)
        
    plt.title('Input Image',FontProperties=title_font)
    
    plt.xticks([])
    plt.yticks([])
    
    '''contrast curve'''
    ax_contrast_curve=plt.subplot(122)
    
    plt.plot(list_VCM_code,
             list_normalized_contrast,
             color=map_mode_color[contrast_operator],
             marker='.',
             markersize=8,
             linestyle='-',
             label=contrast_operator)
    
    #set ticks fonts
    plt.tick_params(labelsize=12)
    labels=ax_contrast_curve.get_xticklabels()+ax_contrast_curve.get_yticklabels()
    
    #label fonts
    [this_label.set_fontname('Times New Roman') for this_label in labels]
        
    plt.title(contrast_operator+' Contrast-VCM Code Curve',FontProperties=title_font)
    
    plt.xlabel('VCM Code',FontProperties=label_font)
    plt.ylabel('Contrast',FontProperties=label_font)
    
    plt.legend(prop=legend_prop,loc='lower right')

    #VMC code for plotting limit 
    list_VCM_code_total=[this_frame.VCM_code for this_frame in frames_coarse]
    
    #limit of x and y
    x_min,x_max=np.min(list_VCM_code_total),np.max(list_VCM_code_total)
    y_min,y_max=0,1
    
    #tick step
    x_major_step=np.ceil((x_max-x_min)/10/50)*50
    x_minor_step=np.ceil((x_max-x_min)/10/50)*25
    y_major_step=0.1
    y_minor_step=0.05
    
    #axis boundary
    plt.xlim([x_min-x_minor_step,x_max+x_minor_step])
    plt.ylim([y_min-y_minor_step,y_max+y_minor_step])
    
    #horizontal line
    plt.hlines(peak_normalized_contrast,
               x_min-x_minor_step,
               x_max+x_minor_step,
               color='grey',
               linestyles="--")
    
    #vertical line
    plt.vlines(peak_VCM_code,
               y_min-y_minor_step,
               y_max+y_minor_step,
               color='grey',
               linestyles="--")

    #set locator
    ax_contrast_curve.xaxis.set_major_locator(MultipleLocator(x_major_step))
    ax_contrast_curve.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
    ax_contrast_curve.yaxis.set_major_locator(MultipleLocator(y_major_step))
    ax_contrast_curve.yaxis.set_minor_locator(MultipleLocator(y_minor_step))
    
    #annotation of peak VCM code
    ax_contrast_curve.annotate('Peak: %d'%peak_VCM_code,
                               xy=(peak_VCM_code,peak_normalized_contrast),
                               xytext=(peak_VCM_code+x_major_step/10,y_major_step/10),
                               color='k',
                               fontproperties=sample_font)
    
    #text of parameter
    ax_contrast_curve.text(list_VCM_code[0]+x_major_step/10,
                           1+y_major_step/10,
                           'ROI Zoom Factor: %d Weight: %.2f-%.2f'%(zoom_factor/2,
                                                                    ROI_weight[0],
                                                                    ROI_weight[1]),
                                                                    FontProperties=text_font)           
                                        
    #save the fig
    '''operator experiment'''
    fig_path_operator=output_folder_operator+'//Peak.png'
    
    '''condition experiment'''
    fig_path_condition=output_folder_condition+str_c+' '+str_d+' (Peak).png'
    
    plt.grid()  
    
    plt.savefig(fig_path_operator,dpi=300,bbox_inches='tight')
    plt.savefig(fig_path_condition,dpi=300,bbox_inches='tight')
    plt.close()
    