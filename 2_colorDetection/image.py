#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 15:13:22 2020

@author: pi
"""

# -*- coding: utf-8 -*-
import numpy as np
import cv2
# 在灰度上加载彩色图像
img = cv2.imread('makerobo1.jpg',0)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
