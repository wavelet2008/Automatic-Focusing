# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:50:07 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: script-AFC Curve
"""

from __init__ import *

import numpy as np
import matplotlib.pyplot as plt

from scipy import interpolate 
from matplotlib.pyplot import MultipleLocator
from configuration_font import text_font,label_font,title_font,sample_font

#------------------------------------------------------------------------------
"""
Calculation Polynomial fitting

Args:
    X: X array
    Y: Y array
    exp: exp index
    n_step: amount of step
    
Returns:
    Parabola Fitting value
"""
def PolynomialFitting(list_x,list_y,exp,n_step=100):
    
    x_min,x_max=np.min(list_x),np.max(list_x)
    
    #polyfit process
    list_x_polyfit=np.linspace(x_min,x_max,n_step)
    list_y_polifit=np.polyval(np.polyfit(list_x,list_y,exp),list_x_polyfit)

    return [[list_x_polyfit[k],list_y_polifit[k]] for k in range(len(list_x_polyfit))] 

#------------------------------------------------------------------------------
"""
B-Spline Interpolation on 1D

Args:
    X: X array
    Y: Y array
    n_step: amount of step
    
Returns:
    Interpolatd coordinates serial
""" 
def BSplineInterpolation(X,Y,n_step=100):
    
    X_new = np.linspace(min(X),max(X),n_step)

    Y_new = interpolate.splev(X_new,interpolate.splrep(X, Y))
    
    return [[X_new[k],Y_new[k]] for k in range(len(X_new))]

#------------------------------------------------------------------------------
"""
P-Chip Interpolation on 1D

Args:
    X: X array
    Y: Y array
    n_step: amount of step
    
Returns:
    Interpolatd coordinates serial
""" 
def PChipInterpolation(X,Y,n_step=100):
    
    X_new = np.linspace(min(X),max(X),n_step)

    Y_new = interpolate.PchipInterpolator(X, Y)(X_new)
    
    return [[X_new[k],Y_new[k]] for k in range(len(X_new))]

'''using that style and plot them'''
list_object_depth=[(k+1)*100 for k in range(10)]

#data from 100mm is from small chart plane, so that dot distance need to mutiply a factor (14/2.8)
list_focus_VCM_code=[850,580,500,460,440,430,410,400,400,400]

list_dot_scale=[2.8]+[14]*9
list_dot_distance=[100.8,231.6,156.0,111.6,89.3,75.5,64.3,55.7,49.3,44.6];

list_image_depth=np.array(list_object_depth)*np.array(list_dot_distance)/np.array(list_dot_scale)*1.2/1000

plt.plot(list_image_depth)

def Curve(list_x,
          list_y,
          str_title,
          str_xlabel,
          str_ylabel):
    
    #limit of x and y
    x_min,x_max=np.min(list_x),np.max(list_x)
    y_min,y_max=np.min(list_y),np.max(list_y)
    
    #tick step
    x_major_step=np.ceil((x_max-x_min)/10/50)*50
    x_minor_step=np.ceil((x_max-x_min)/10/50)*25
    
    scale='macro'
    
    if y_max-y_min<1:
        
        scale='micro'
        
    if scale=='macro':
        
        y_major_step=np.ceil((y_max-y_min)/10/50)*50
        y_minor_step=np.ceil((y_max-y_min)/10/50)*25
        
    if scale=='micro':
        
        y_major_step=np.ceil((y_max-y_min)*50)/10/50
        y_minor_step=np.ceil((y_max-y_min)*25)/10/50
        
    plt.figure(figsize=(13,6))
    
    '''p-chip interpolation'''
    # smoothed_x_y=PChipInterpolation(list_x,list_y)
    
    # x_smoothed=[this_x_y[0] for this_x_y in smoothed_x_y]
    # y_smoothed=[this_x_y[1] for this_x_y in smoothed_x_y] 
    
    # plt.plot(x_smoothed,y_smoothed,'grey')
    
    '''polynomial fitting'''
    # polyfitted_x_y=PolynomialFitting(list_x,list_y,3,100)
    
    # x_polyfitted=[this_x_y[0] for this_x_y in polyfitted_x_y]
    # y_polyfitted=[this_x_y[1] for this_x_y in polyfitted_x_y] 

    # plt.plot(x_polyfitted,y_polyfitted,color='grey')
    
    '''optimize fitting'''
    from scipy.optimize import curve_fit
    
    def func(x, a, b, c):
        
        return c+b/(x)
    
    x_min,x_max=np.min(list_x),np.max(list_x)
    
    #polyfit process
    list_x_polyfit=np.linspace(x_min,x_max,100)
    
    # 曲线拟合，popt为函数的参数list
    popt, pcov = curve_fit(func, list_x, list_y)
    
    # 直接用函数和函数参数list来进行y值的计算
    y_pred = [func(i, popt[0], popt[1], popt[2]) for i in list_x_polyfit] 
    
    plt.plot(list_x_polyfit,y_pred,color='grey')
    
    for k in range(len(list_x)):
        
        plt.scatter(list_x[k],list_y[k],color='k')
        
        if scale=='micro':
            
            value_format='%.2f'
            
        if scale=='macro':
            
            value_format='%.d'
            
        plt.annotate(value_format%list_y[k],
                     xy=(list_x[k],list_y[k]),
                     xytext=(list_x[k]+0.1*x_major_step,
                             list_y[k]+0.1*y_major_step),
                     color='k',
                     fontproperties=sample_font)
        
    ax=plt.gca()
    
    ax.xaxis.set_major_locator(MultipleLocator(x_major_step))
    ax.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
    ax.yaxis.set_major_locator(MultipleLocator(y_major_step))
    ax.yaxis.set_minor_locator(MultipleLocator(y_minor_step))
    
    #axis boundary
    plt.xlim([x_min-x_minor_step,x_max+x_minor_step])
    plt.ylim([y_min-y_minor_step,y_max+y_minor_step])  
     
    #set ticks fonts
    plt.tick_params(labelsize=12)
    labels=ax.get_xticklabels()+ax.get_yticklabels()
    
    #label fonts
    [this_label.set_fontname('Times New Roman') for this_label in labels]
        
    plt.title(str_title,FontProperties=title_font)
    
    plt.xlabel(str_xlabel,FontProperties=label_font)
    plt.ylabel(str_ylabel,FontProperties=label_font)

    #show the grid
    plt.grid()
    plt.show()
    
#plot curve of Focus VCM Code-Object Depth Curve
Curve(list_object_depth,
      list_focus_VCM_code,
      'Focus VCM Code-Object Depth Curve',
      'Object Depth (mm)',
      'Focus VCM Code (--)')

#plot curve of Dot Distance-Object Depth Curve
Curve(list_object_depth,
      list_image_depth,
      'Image Depth-Object Depth Curve',
      'Object Depth (mm)',
      'Image Depth (mm)')

