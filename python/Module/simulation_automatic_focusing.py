# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 17:54:22 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Simulation of AutoFocus
"""

import os
import imageio
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import MultipleLocator

import operation_path as O_P
import operation_import as O_I

import calculation_contrast as C_C
import calculation_peak_search as C_P_S
import calculation_numerical_analysis as C_N_A

from configuration_font import legend_prop,\
                               text_prop,\
                               label_prop,\
                               title_prop,\
                               annotation_prop

from configuration_color import map_operator_color,\
                                list_contrast_operator,\
                                list_tenengrad_operator

from calculation_contrast import zoom_factor,\
                                 ROI_weight_5_area,\
                                 ROI_weight_9_area

#------------------------------------------------------------------------------
"""
Plot animation of movement of lens

Args:
   imgs_folder: folder which contains a batch of images 
   operator: operator of contrast or tenengrad calculation 
   ROI mode: definition method of ROI ['5-Area', 'Center']
   peak_search_method: method of peak search
   
Returns:
    None
"""
def LensAnimation(imgs_folder,operator,ROI_mode,peak_search_method):
    
    print('')
    print('-- Lens Animation')
    print('-> operator:',operator)
    print('-> ROI mode:',ROI_mode)
    print('-> peak search method:',peak_search_method)
    print('')
    
    str_a,str_b=imgs_folder.split('Material')
    str_c,str_d=imgs_folder.split('Material')[-1].strip('\\').split('\\')

    #construct output folder
    output_folder_operator=str_a+'\\Lens Animation\\Scenario'+str_b
    
    try:
        
        output_folder_condition=output_folder_operator.split(str_c)[0].replace('\\Scenario','')+'\\Operator'
    
    except:
        
        output_folder_condition=str_a+'\\Lens Animation\Operator'
    
    output_folder_operator+='\\'+operator+'\\'
    output_folder_condition+='\\'+operator+'\\'
    
    O_P.GenerateFolder(output_folder_operator)
    O_P.GenerateFolder(output_folder_condition)
    
    #frame object for coarse and fine search
    list_frame=O_I.FramesConstruction(imgs_folder,operator,ROI_mode)
    list_contrast=[this_frame.focus_value for this_frame in list_frame]
    
    '''Global Search (Full Sweep)'''
    if peak_search_method=='Global':
        
        list_index_plotted=C_P_S.GlobalSearch(list_contrast)
        abbr_method='GS'
        
    '''Coarse to Fine Search'''
    if peak_search_method=='Coarse2Fine':
        
        list_index_plotted=C_P_S.Coarse2FineSearch(list_contrast)
        abbr_method='C2F'
        
    '''Binary Search (Fibonacci)'''
    if peak_search_method=='Binary':
        
        list_index_plotted=C_P_S.BinarySearch(list_contrast)
        abbr_method='BS'
    
    list_frame_plotted=[list_frame[this_index] for this_index in list_index_plotted]
    list_code_plotted=[this_frame.lens_position_code for this_frame in list_frame_plotted]  

    '''plot lens'''
    len_major=6
    len_minor=1
    width=23
    
    figures=[]
    
    #limit of x and y
    x_min,x_max=-24,1024
    y_min,y_max=-5,5
    
    for lens_position in list_code_plotted:
        
        pos_A=[lens_position+width/2,-len_major/2+len_minor/2]
        pos_B=[lens_position+width/2,+len_major/2+len_minor/2]
        pos_C=[lens_position-width/2,+len_major/2-len_minor/2]
        pos_D=[lens_position-width/2,-len_major/2-len_minor/2]
        
        list_corner_quadrangle=[pos_A,pos_B,pos_C,pos_D,pos_A]
        
        plt.figure(figsize=(23,3))
        
        for k in range(4):
            
            last_point=list_corner_quadrangle[k]
            next_point=list_corner_quadrangle[k+1]
            
            plt.plot([last_point[0],next_point[0]],
                     [last_point[1],next_point[1]],'k-')
        
        plt.yticks([])
        plt.xticks([])
        
        plt.xlim([0,1024])
        plt.ylim([-5,5])   
        
        #horizontal line
        plt.hlines(0,
                   x_min,
                   x_max,
                   color='grey',
                   linestyles="--")
        
        #vertical line
        plt.vlines(lens_position,
                    y_min,
                    y_max,
                    color='grey',
                    linestyles="--")

        #save the fig
        this_fig_path=output_folder_operator+'//Lens %d.png'%(lens_position)
        
        plt.savefig(this_fig_path,dpi=300,bbox_inches='tight')
        plt.close()
        
        #collect fig to create GIF
        figures.append(imageio.imread(this_fig_path))
    
    '''operator experiment'''
    fig_path_operator=output_folder_operator+'//%s.gif'%peak_search_method
    
    '''condition experiment'''
    fig_path_condition=output_folder_condition+'%s %s (%s).gif'%(str_c,str_d,peak_search_method)
    
    #save GIF 
    '''operator experiment'''
    imageio.mimsave(fig_path_operator,figures,duration=0.23) 
    
    '''scenario experiment'''
    imageio.mimsave(fig_path_condition,figures,duration=0.23) 
    
#------------------------------------------------------------------------------
"""
Plot animation field of FOV

Args:
   imgs_folder: folder which contains a batch of images 
   operator: operator of contrast or tenengrad calculation 
   ROI mode: definition method of ROI ['5-Area', 'Center']
   peak_search_method: method of peak search
   
Returns:
    None
"""
def FOVAnimation(imgs_folder,operator,ROI_mode,peak_search_method):
    
    print('')
    print('-- AF Animation')
    print('-> operator:',operator)
    print('-> ROI mode:',ROI_mode)
    print('-> peak search method:',peak_search_method)
    print('')
    
    str_a,str_b=imgs_folder.split('Material')
    str_c,str_d=imgs_folder.split('Material')[-1].strip('\\').split('\\')

    #construct output folder
    output_folder_operator=str_a+'\\AF Simulation\\Scenario'+str_b
    
    try:
        
        output_folder_condition=output_folder_operator.split(str_c)[0].replace('\\Scenario','')+'\\Operator'
    
    except:
        
        output_folder_condition=str_a+'\\AF Simulation\Operator'
    
    output_folder_operator+='\\'+operator+'\\'
    output_folder_condition+='\\'+operator+'\\'
    
    O_P.GenerateFolder(output_folder_operator)
    O_P.GenerateFolder(output_folder_condition)
    
    #frame object for coarse and fine search
    list_frame=O_I.FramesConstruction(imgs_folder,operator,ROI_mode)
    list_contrast=[this_frame.focus_value for this_frame in list_frame]
    
    '''Global Search (Full Sweep)'''
    if peak_search_method=='Global':
        
        list_index_plotted=C_P_S.GlobalSearch(list_contrast)
        abbr_method='GS'
        
    '''Coarse to Fine Search'''
    if peak_search_method=='Coarse2Fine':
        
        list_index_plotted=C_P_S.Coarse2FineSearch(list_contrast)
        abbr_method='C2F'
        
    '''Binary Search (Fibonacci)'''
    if peak_search_method=='Binary':
        
        list_index_plotted=C_P_S.BinarySearch(list_contrast)
        abbr_method='BS'
    
    figures=[]
    
    for k in range(len(list_index_plotted)):
        
        list_frame_plotted=[list_frame[this_index] for this_index in list_index_plotted][:k+1]
        list_code_plotted=[this_frame.lens_position_code for this_frame in list_frame_plotted]    
        list_contrast_plotted=[this_frame.focus_value for this_frame in list_frame_plotted]

        #normalization of contrast list
        list_normalized_contrast_plotted=C_N_A.Normalize(list_contrast_plotted)
    
        plt.figure(figsize=(17,6))
        
        #limit of x and y
        x_min,x_max=-24,1024
        y_min,y_max=0-.023*2,1+.023*2
        
        #tick step
        x_major_step=100
        x_minor_step=50
        y_major_step=0.1
        y_minor_step=0.05
        
        #text of parameter
        if ROI_mode=='5-Area':
                    
            str_text='ROI Zoom Factor: %d Weight: %.2f-%.2f'%(zoom_factor/2,
                                                              ROI_weight_5_area[0],
                                                              ROI_weight_5_area[1])
        
        if ROI_mode=='9-Area':
                    
            str_text='ROI Zoom Factor: %d Weight: %.2f-%.2f'%(zoom_factor/2,
                                                              ROI_weight_9_area[4],
                                                              ROI_weight_9_area[0])
            
        if ROI_mode=='Center':              
    
            str_text='ROI Zoom Factor: %d'%(zoom_factor/2) 
            
        '''input image and bound'''
        ax_input_image=plt.subplot(121)
        
        plt.imshow(list_frame_plotted[k].img_gray,cmap='gray')
        plt.imshow(list_frame_plotted[k].img_ROI,cmap='seismic_r') 
        
        plt.title('Input Image',fontdict=title_prop)
        
        plt.xticks([])
        plt.yticks([])
        
        '''contrast curve'''
        ax_contrast_curve=plt.subplot(122)
        
        #set ticks fonts
        plt.tick_params(labelsize=12)
        labels=ax_contrast_curve.get_xticklabels()+ax_contrast_curve.get_yticklabels()
        
        #label fonts
        [this_label.set_fontname('Times New Roman') for this_label in labels]
            
        plt.xlabel('Lens Position Code',fontdict=label_prop)   
        plt.ylabel('Focus Value',fontdict=label_prop)
        
        if operator in list_contrast_operator:
            
            str_focus_value=operator+' Contrast'
            
        if operator in list_tenengrad_operator:
            
            str_focus_value=operator+' Tenengrad'
                
        plt.title('Focus Value-Lens Position Curve',fontdict=title_prop)
        
        plt.plot(list_code_plotted,
                 list_normalized_contrast_plotted,
                 color=map_operator_color[operator],
                 marker='.',
                 markersize=8,
                 linestyle='-',
                 label=str_focus_value)
        
        plt.legend(prop=legend_prop,loc='lower right')
    
        #axis boundary
        plt.xlim([x_min,x_max])
        plt.ylim([y_min,y_max])

        #set locator
        ax_contrast_curve.xaxis.set_major_locator(MultipleLocator(x_major_step))
        ax_contrast_curve.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
        ax_contrast_curve.yaxis.set_major_locator(MultipleLocator(y_major_step))
        ax_contrast_curve.yaxis.set_minor_locator(MultipleLocator(y_minor_step))

        #basic parameter                     
        ax_contrast_curve.text(0+x_major_step/10,
                               0+y_major_step/10,
                               str_text,
                               fontdict=annotation_prop) 

        #peak search parameter
        ax_contrast_curve.text(0+x_major_step/10,
                               1+y_major_step/10,
                               'Method: %s Iter: %d'%(abbr_method,k),
                               fontdict=text_prop)
        
        #save the fig
        this_fig_path=output_folder_operator+'//Lens %d.png'%(list_code_plotted[k])
        
        plt.grid()
        
        plt.savefig(this_fig_path,dpi=300,bbox_inches='tight')
        plt.close()
        
        #collect fig to create GIF
        figures.append(imageio.imread(this_fig_path))
        
    '''operator experiment'''
    fig_path_operator=output_folder_operator+'//%s.gif'%peak_search_method
    
    '''condition experiment'''
    fig_path_condition=output_folder_condition+'%s %s (%s).gif'%(str_c,str_d,peak_search_method)
    
    #save GIF   
    '''operator experiment'''
    imageio.mimsave(fig_path_operator,figures,duration=0.23) 
    
    '''scenario experiment'''
    imageio.mimsave(fig_path_condition,figures,duration=0.23) 
    
#------------------------------------------------------------------------------
"""
Plot input image as well as contrast curve

Args:
   imgs_folder: folder which contains a batch of images 
   operator: operator of contrast calculation 
   ROI mode: definition method of ROI ['5-Area', 'Center']
   
Returns:
    None
"""
def AutoFocusAnimation(imgs_folder,operator,ROI_mode):
    
    print('')
    print('-- Image And Contrast')
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

    if list_imgs_folder==[]:
        
        list_imgs_folder=[imgs_folder]

    #construct frame objects
    frames=O_I.CombineFrames(list_imgs_folder)

    #total data of frames
    list_VCM_code=[]
    list_contrast=[]
    list_img_ROI=[]

    if operator not in list_operator:
        
        return print('=> ERROR: Incorrect Operator')
        
    #traverse all frames
    for this_frame in frames:
        
        img_gray=this_frame.img_gray
           
        #size of img
        height,width=np.shape(img_gray)
        
        #basic parameters
        ROI_weight=[0.44,0.14,0.14,0.14,0.14]
        zoom_factor=16
        ROI_linewidth=int(height//300)
        text_position='Contrast'
   
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
        
        list_VCM_code.append(this_frame.VCM_code)
        
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
            list_contrast.append(np.sum(np.array(ROI_weight)*np.array(list_contrast_5_areas)))
            list_img_ROI.append(this_img_ROI)
            
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
            list_contrast.append(list_contrast_5_areas[0])
            list_img_ROI.append(this_img_ROI)
        
    #center of ROI
    list_5_center_ROI=[[ height/2, width/2],
                       [  height/4,   width/4],
                       [  height/4, 3*width/4],
                       [3*height/4, 3*width/4],
                       [3*height/4,   width/4]]
    
    #figs to make animation
    figures=[]
    
    #traverse again and make visualization
    for k in range(len(frames)):
        
        print('--> VCM Code:',list_VCM_code[k])
        
        #init real-time data
        list_VCM_code_this_frame=list_VCM_code[:k+1]
        list_normalized_contrast_this_frame=C_N_A.Normalize(list_contrast[:k+1])
        img_ROI_this_frame=list_img_ROI[k]
        
        if pre_fix=='':
        
            list_VCM_code_this_frame=list(np.array(C_N_A.Normalize(list_VCM_code_this_frame))*1024)
        
        plt.figure(figsize=(17,6))
        
        '''input image'''
        ax_input_image=plt.subplot(121)
        plt.imshow(frames[k].img_gray,cmap='gray')
        
        #ROI bound
        plt.imshow(img_ROI_this_frame,cmap='seismic_r')
        
        if text_position=='Image':
        
            #show ROI weight
            for kk in range(len(list_5_center_ROI)):
                
                #center coordinates of ROI
                y_center_ROI=list_5_center_ROI[kk][0]+height/60
                x_center_ROI=list_5_center_ROI[kk][1]-width/40
                
                ax_input_image.text(x_center_ROI,
                                    y_center_ROI,
                                    '%.2f'%(ROI_weight[kk]),
                                    fontproperties=text_prop)
            
        plt.title('Input Image',FontProperties=title_prop)
        
        plt.xticks([])
        plt.yticks([])
        
        '''contrast curve'''
        ax_contrast_curve=plt.subplot(122)

        plt.plot(list_VCM_code_this_frame,
                 list_normalized_contrast_this_frame,
                 color=map_operator_color[operator],
                 marker='.',
                 markersize=8,
                 linestyle='-',
                 label=operator)
        
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
        
        #set ticks fonts
        plt.tick_params(labelsize=12)
        labels=ax_contrast_curve.get_xticklabels()+ax_contrast_curve.get_yticklabels()
        
        #label fonts
        [this_label.set_fontname('Times New Roman') for this_label in labels]
            
        plt.xlabel('Lens Position Code',fontdict=label_prop)   
        plt.ylabel('Focus Value',fontdict=label_prop)
        
        if operator in list_contrast_operator:
            
            str_focus_value=operator+' Contrast'
            
        if operator in list_tenengrad_operator:
            
            str_focus_value=operator+' Tenengrad'
            
        plt.title(str_focus_value+'-Lens Position Curve',fontdict=title_prop)
    
        plt.legend(prop=legend_prop,loc='lower right')
  
        #set locator
        ax_contrast_curve.xaxis.set_major_locator(MultipleLocator(x_major_step))
        ax_contrast_curve.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
        ax_contrast_curve.yaxis.set_major_locator(MultipleLocator(y_major_step))
        ax_contrast_curve.yaxis.set_minor_locator(MultipleLocator(y_minor_step))
        
        #text of parameter
        if text_position=='Contrast':
            
            if ROI_mode=='5-Area':
                
                str_text='ROI Zoom Factor: %d Weight: %.2f-%.2f'%(zoom_factor/2,ROI_weight[0],ROI_weight[1])
                
            if ROI_mode=='Center':              

                str_text='ROI Zoom Factor: %d'%(zoom_factor/2)   
                                        
            ax_contrast_curve.text(0+x_major_step/10,
                                   1+y_major_step/10,
                                   str_text,
                                   FontProperties=text_prop)               
        
        #save the fig
        this_fig_path=output_folder_operator+'//%d.png'%(list_VCM_code[k])
        
        plt.grid()
        
        plt.savefig(this_fig_path,dpi=300,bbox_inches='tight')
        plt.close()
        
        #collect fig to create GIF
        figures.append(imageio.imread(this_fig_path))
        
    #save GIF 
    '''operator experiment'''
    imageio.mimsave(output_folder_operator+'\\'+operator+'.gif',figures,duration=0.1) 
    
    '''condition experiment'''
    imageio.mimsave(output_folder_condition+str_c+' '+str_d+'.gif',figures,duration=0.1) 