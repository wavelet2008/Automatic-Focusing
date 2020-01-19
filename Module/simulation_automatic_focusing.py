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
from matplotlib.font_manager import FontProperties

import operation_path as O_P
import operation_import as O_I

import calculation_contrast as C_C
import calculation_numerical_analysis as C_N_A

#font of fonts of all kinds
legend_prop={'family':'Gill Sans MT','weight':'normal','size':12}
text_font=FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=12)
label_font=FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=16)
title_font=FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=18)

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
Plot input image as well as contrast curve

Args:
   imgs_folder: folder which contains a batch of images 
   contrast_operator: operator of contrast calculation 
   
Returns:
    None
"""
def ImageAndContrast(imgs_folder,contrast_operator):
    
    print('')
    print('-- Image And Contrast')
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
    frames=O_I.CombineFrames(list_imgs_folder)

    #total data of frames
    list_VCM_code=[]
    list_contrast=[]
    list_img_ROI=[]

    if contrast_operator not in list_contrast_operator:
        
        return print('=> ERROR: Incorrect Input')
        
    #traverse all frames
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
        list_VCM_code.append(this_frame.VCM_code)
        list_contrast.append(np.sum(np.array(ROI_weight)*np.array(list_contrast_5_areas)))
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
                                    fontproperties=text_font)
            
        plt.title('Input Image',FontProperties=title_font)
        
        plt.xticks([])
        plt.yticks([])
        
        '''contrast curve'''
        ax_contrast_curve=plt.subplot(122)

        plt.plot(list_VCM_code_this_frame,
                 list_normalized_contrast_this_frame,
                 color=map_mode_color[contrast_operator],
                 marker='.',
                 markersize=8,
                 linestyle='-',
                 label=contrast_operator)
        
        #limit of x and y
        x_min,x_max=np.min(list_VCM_code),np.max(list_VCM_code)
        y_min,y_max=0,1
        
        #tick step
        x_major_step=np.ceil((x_max-x_min)/10/50)*50
        x_minor_step=np.ceil((x_max-x_min)/10/50)*25
        y_major_step=0.1
        y_minor_step=0.05
        
        #axis boundary
        plt.xlim([x_min-x_minor_step,x_max+x_minor_step])
        plt.ylim([y_min-y_minor_step,y_max+y_minor_step])  
        
        #set ticks fonts
        plt.tick_params(labelsize=12)
        labels=ax_contrast_curve.get_xticklabels()+ax_contrast_curve.get_yticklabels()
        
        #label fonts
        [this_label.set_fontname('Times New Roman') for this_label in labels]
            
        plt.title(contrast_operator+' Contrast-VCM Code Curve',FontProperties=title_font)
        
        plt.xlabel('VCM Code',FontProperties=label_font)
        plt.ylabel('Contrast',FontProperties=label_font)
        
        plt.legend(prop=legend_prop,loc='lower right')
  
        #set locator
        ax_contrast_curve.xaxis.set_major_locator(MultipleLocator(x_major_step))
        ax_contrast_curve.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
        ax_contrast_curve.yaxis.set_major_locator(MultipleLocator(y_major_step))
        ax_contrast_curve.yaxis.set_minor_locator(MultipleLocator(y_minor_step))
        
        #text of parameter
        if text_position=='Contrast':
            
            ax_contrast_curve.text(list_VCM_code[0]+x_major_step/10,
                                   1+y_major_step/10,
                                   'ROI Zoom Factor: %d Weight: %.2f-%.2f'%(zoom_factor/2,
                                                                            ROI_weight[0],
                                                                            ROI_weight[1]),
                                                                            FontProperties=text_font)               
        
        #save the fig
        this_fig_path=output_folder_operator+'//%d.png'%(list_VCM_code[k])
        
        plt.grid()
        
        plt.savefig(this_fig_path,dpi=300,bbox_inches='tight')
        plt.close()
        
        #collect fig to create GIF
        figures.append(imageio.imread(this_fig_path))
        
    #save GIF 
    '''operator experiment'''
    imageio.mimsave(output_folder_operator+'\\'+contrast_operator+'.gif',figures,duration=0.1) 
    
    '''condition experiment'''
    imageio.mimsave(output_folder_condition+str_c+' '+str_d+'.gif',figures,duration=0.1) 