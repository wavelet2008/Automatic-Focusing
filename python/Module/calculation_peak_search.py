# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 17:00:27 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Search of contrast peak value
"""

import os
import copy as cp
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import MultipleLocator

import operation_path as O_P
import operation_import as O_I
import operation_dictionary as O_D

import calculation_contrast as C_C
import calculation_numerical_analysis as C_N_A

from configuration_font import legend_prop,text_font,label_font,title_font,sample_font
from configuration_color import map_operator_color,list_operator,list_contrast_operator,list_articulation_operator

#------------------------------------------------------------------------------
"""
Preprocessing in peak search to tolerate one fluctuation in ascending

Args:
    list_contrast: contrast value list
    
Returns:
    new contrast list after processing
"""
def PreProcessing(list_contrast):
    
    #final result
    list_contrast_new=[list_contrast[0]]
    
    for k in range(1,len(list_contrast)-1):
        
        #replace the particular with the average
        if list_contrast[k]<list_contrast[k-1]<list_contrast[k+1]:
            
            list_contrast_new.append(0.5*(list_contrast[k-1]+list_contrast[k+1]))
        
        else:
            
            list_contrast_new.append(list_contrast[k])
            
    return list_contrast_new+[list_contrast[-1]]

#------------------------------------------------------------------------------
"""
Postprocessing in peak search to tolerate one fluctuation in ascending

Args:
    list_contrast: contrast value list
    
Returns:
    new contrast list after processing
"""
def PostProcessing(list_contrast):

    #final result
    list_contrast_new=[list_contrast[0]]
    
    for k in range(1,len(list_contrast)-1):
        
        #replace the particular with the average
        if list_contrast[k]>list_contrast[k-1]>list_contrast[k+1]:
            
            list_contrast_new.append(0.5*(list_contrast[k-1]+list_contrast[k+1]))
        
        else:
            
            list_contrast_new.append(list_contrast[k])
            
    return list_contrast_new+[list_contrast[-1]]

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
    amount_revert=3
    
    #real-time
    amount_ascending,amount_descending=0,0
    
    #strat and end point for fine search
    index_a,index_b=None,None
    
    #index of maximum
    index_maximum=list_contrast.index(np.max(list_contrast))

    # '''preprocessing: try to tolerate one fluctuation in ascending'''
    # if len(list_contrast)>=3:
        
    #     list_contrast=PreProcessing(list_contrast)

    for k in range(len(list_contrast)-1):
        
        '''ascending'''
        if list_contrast[k]<list_contrast[k+1]:
            
            amount_ascending+=1
            amount_descending=0  
                    
        if list_contrast[k]==list_contrast[k+1]:
        
            continue
        
        '''descending'''
        if list_contrast[k]>list_contrast[k+1]:
            
            amount_descending+=1
            amount_ascending=0
        
        #end index of ascending
        if amount_ascending>=amount_revert:

            index_a=k+1
   
        #start index of descending
        if amount_descending>=amount_revert:
            
            index_b=k-amount_descending+1

        # ''''postprocessing: try to tolerate one fluctuation in descending'''
        # if index_a!=None:

        #     list_contrast=list_contrast[:index_a]+PostProcessing(list_contrast[index_a:])
        
    if index_a!=None and index_b!=None:

        #expire the exception
        if index_a==index_maximum and index_b==index_maximum:
            
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
   operator: operator of contrast or articulation calculation 
   ROI mode: definition method of ROI ['5-Area', 'Center']
   
Returns:
    None
"""
def FullSweep(imgs_folder,operator,ROI_mode):
    
    print('')
    print('-- Full Sweep')
    print('-> Operator:',operator)
    
    str_a,str_b=imgs_folder.split('Experiment')
    str_c,str_d=imgs_folder.split('Experiment')[-1].strip('\\').split('\\')

    #construct output folder
    output_folder_operator=str_a+'\\Contrast\\Scenario'+str_b
    
    try:
        
        output_folder_condition=output_folder_operator.split(str_c)[0].replace('\\Scenario','')+'\\Operator'
    
    except:
        
        output_folder_condition=str_a+'\\Contrast\Operator'
    
    output_folder_operator+='\\'+operator+'\\'
    output_folder_condition+='\\'+operator+'\\'
    
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
        
        print('=> WARNING: No both Corase and Fine Folder')
        
        imgs_folder_coarse=cp.deepcopy(imgs_folder)

    #frame object for coarse and fine search
    frames_coarse=O_I.FramesConstruction(imgs_folder_coarse)
    
    try:
        
        frames_fine=O_I.FramesConstruction(imgs_folder_fine)
    
    except:
        
        pass
    
    #total data of coarse frames
    list_VCM_code_coarse=[]
    list_contrast_coarse=[]
    list_img_ROI_coarse=[]

    if operator not in list_operator:
        
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
        zoom_factor=16
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
        
        list_VCM_code_coarse.append(this_frame.VCM_code)
        
        #calculate contrast in each area
        list_contrast_5_areas=[] 
        
        if ROI_mode=='5-Area':
            
            for i,j in list_5_points:
                        
                this_area=img_gray[int(i)-area_half_height:int(i)+area_half_height,
                                   int(j)-area_half_width:int(j)+area_half_width]
            
                #collect it
                list_contrast_5_areas.append(C_C.GlobalContrast(this_area,operator))
            
                #draw the bound of ROI
                for k in range(ROI_linewidth):
                    
                    this_img_ROI[int(i-k)-area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                    this_img_ROI[int(i+k)+area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                    this_img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j-k)-area_half_width]=1
                    this_img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j+k)+area_half_width]=1
      
            #collect the data
            list_contrast_coarse.append(np.sum(np.array(ROI_weight)*np.array(list_contrast_5_areas)))
            list_img_ROI_coarse.append(this_img_ROI)
       
        if ROI_mode=='Center':
            
            for i,j in list_5_points[:1]:
                        
                this_area=img_gray[int(i)-area_half_height:int(i)+area_half_height,
                                   int(j)-area_half_width:int(j)+area_half_width]
            
                #collect it
                list_contrast_5_areas.append(C_C.GlobalContrast(this_area,operator))
            
                #draw the bound of ROI
                for k in range(ROI_linewidth):
                    
                    this_img_ROI[int(i-k)-area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                    this_img_ROI[int(i+k)+area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                    this_img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j-k)-area_half_width]=1
                    this_img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j+k)+area_half_width]=1
      
            #collect the data
            list_contrast_coarse.append(list_contrast_5_areas[0])
            list_img_ROI_coarse.append(this_img_ROI)
            
        #result of full sweep
        result_full_sweep=FullSweepCoarse(list_contrast_coarse)
        
        print('--> VCM Code:',this_frame.VCM_code)
        # print('---> Contrast:',list_contrast_coarse[-1])
        
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
    
    try:
        
        for this_frame in frames_fine:
            
            if VCM_code_start<=this_frame.VCM_code<=VCM_code_end:
                
                frames.append(this_frame)
                
    except:
        
        for this_frame in frames_coarse:
            
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
            zoom_factor=16
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
            
            list_VCM_code_fine.append(this_frame.VCM_code)
            
            #calculate contrast in each area
            list_contrast_5_areas=[]
            
            if ROI_mode=='5-Area':
                
                for i,j in list_5_points:
                            
                    this_area=img_gray[int(i)-area_half_height:int(i)+area_half_height,
                                       int(j)-area_half_width:int(j)+area_half_width]
                
                    #collect it
                    list_contrast_5_areas.append(C_C.GlobalContrast(this_area,operator))
                
                    #draw the bound of ROI
                    for k in range(ROI_linewidth):
                        
                        this_img_ROI[int(i-k)-area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                        this_img_ROI[int(i+k)+area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                        this_img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j-k)-area_half_width]=1
                        this_img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j+k)+area_half_width]=1
        
                #collect the data
                list_contrast_fine.append(np.sum(np.array(ROI_weight)*np.array(list_contrast_5_areas)))
                list_img_ROI_fine.append(this_img_ROI)
           
            if ROI_mode=='Center':
                
                for i,j in list_5_points[:1]:
                            
                    this_area=img_gray[int(i)-area_half_height:int(i)+area_half_height,
                                       int(j)-area_half_width:int(j)+area_half_width]
                
                    #collect it
                    list_contrast_5_areas.append(C_C.GlobalContrast(this_area,operator))
                
                    #draw the bound of ROI
                    for k in range(ROI_linewidth):
                        
                        this_img_ROI[int(i-k)-area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                        this_img_ROI[int(i+k)+area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                        this_img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j-k)-area_half_width]=1
                        this_img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j+k)+area_half_width]=1
        
                #collect the data
                list_contrast_fine.append(list_contrast_5_areas[0])
                list_img_ROI_fine.append(this_img_ROI)
                
            print('--> VCM Code:',this_frame.VCM_code)
            # print('---> Contrast:',list_contrast_fine[-1])
            
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
        
    print('')
    print('---> Peak VCM Code:',peak_VCM_code)
    
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
             color=map_operator_color[operator],
             marker='.',
             markersize=8,
             linestyle='-',
             label=operator)
    
    #set ticks fonts
    plt.tick_params(labelsize=12)
    labels=ax_contrast_curve.get_xticklabels()+ax_contrast_curve.get_yticklabels()
    
    #label fonts
    [this_label.set_fontname('Times New Roman') for this_label in labels]
    
    plt.xlabel('VCM Code',FontProperties=label_font)   
    
    if operator in list_contrast_operator:
        
        plt.title(operator+' Contrast-VCM Code Curve',FontProperties=title_font)

        plt.ylabel('Contrast',FontProperties=label_font)
        
    if operator in list_articulation_operator:
        
        plt.title(operator+' Articulation-VCM Code Curve',FontProperties=title_font)

        plt.ylabel('Articulation',FontProperties=label_font)
        
    plt.legend(prop=legend_prop,loc='lower right')

    #VMC code for plotting limit 
    list_VCM_code_total=[this_frame.VCM_code for this_frame in frames_coarse]

    #limit of x and y
    x_min,x_max=-24,1024
    y_min,y_max=0-.023*2,1+.023*2
    
    #tick step
    x_major_step=100
    x_minor_step=50
    y_major_step=0.1
    y_minor_step=0.05
    
    #axis boundary
    plt.xlim([x_min,x_max])
    plt.ylim([y_min,y_max])
    
    #horizontal line
    plt.hlines(peak_normalized_contrast,
               x_min,
               x_max,
               color='grey',
               linestyles="--")
    
    #vertical line
    plt.vlines(peak_VCM_code,
               y_min,
               y_max,
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
                               xytext=(peak_VCM_code+x_major_step/10,peak_normalized_contrast+y_major_step/10),
                               color='k',
                               fontproperties=sample_font)
    
    #text of parameter
    if ROI_mode=='5-Area':
                
        str_text='ROI Zoom Factor: %d Weight: %.2f-%.2f'%(zoom_factor/2,ROI_weight[0],ROI_weight[1])
        
    if ROI_mode=='Center':              

        str_text='ROI Zoom Factor: %d'%(zoom_factor/2)   
                                     
    ax_contrast_curve.text(0+x_major_step/10,
                           1+y_major_step/10,
                           str_text,
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
    