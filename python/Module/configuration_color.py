# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 17:03:23 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Cofiguration of contrast operator and their color
"""

#contrast
list_contrast_operator=['KK',
                        'Whittle',
                        'Burkhardt',
                        'Michelson',
                        'Peli',
                        'W3C',
                        'Weber',
                        'Stevens',
                        'Boccignone',
                        'GLCM',
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
                        'Rizzi',
                        'CMSL',
                        'CMAN']
        
list_contrast_color=['tan',
                     'cyan',
                     'teal',
                     'olive',
                     'maroon',
                     'orchid',
                     'sienna',
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
                     'oliverdrab',
                     'lightsalmon',
                     'mediumvioletred',
                     'mediumslateblue',
                     'mediumturquoise',
                     'mediumaquamarine']

#articulation
list_tenengrad_operator=['Canny',
                         'Sobel',
                         'Sobel-x',
                         'Sobel-y',
                         'Laplacian']

list_tenengrad_color=['plum',
                      'bisque',
                      'indigo',
                      'sienna',
                      'magenta']  

#texture feature
list_texture_feature_operator=['ASM',
                               'Contrast',
                               'Energy',
                               'IDM']

list_texture_feature_color=['brown',
                            'coral',
                            'hotpink',
                            'indianred']

#map between mode and color   
map_contrast_color=dict(zip(list_contrast_operator,list_contrast_color)) 

map_tenengrad_color=dict(zip(list_tenengrad_operator,list_tenengrad_color)) 

map_texture_feature_color=dict(zip(list_texture_feature_operator,list_texture_feature_color)) 

list_operator=list_contrast_operator+\
              list_tenengrad_operator+\
              list_texture_feature_operator
              
map_operator_color={**map_contrast_color,
                    **map_tenengrad_color,
                    **map_texture_feature_color}