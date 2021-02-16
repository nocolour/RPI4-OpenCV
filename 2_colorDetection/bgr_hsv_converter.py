#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：40_colorDetection.py
#  版本：V2.0
#  author: zhulin
#  说明：颜色检测
#####################################################
"""

import sys
import numpy as np
import cv2
 
blue = sys.argv[1]
green = sys.argv[2]
red = sys.argv[3]  
 
color = np.uint8([[[blue, green, red]]])
hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
 
hue = hsv_color[0][0][0]
 
print(("Lower bound is :"), end=' ')
print(("[" + str(hue-10) + ", 100, 100]\n"))
 
print(("Upper bound is :"), end=' ')
print(("[" + str(hue + 10) + ", 255, 255]"))
