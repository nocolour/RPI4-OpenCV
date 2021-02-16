#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：39_simpleCamtest.py
#  版本：V2.0
#  author: zhulin
#  说明：测试摄像头实验
#####################################################
"""

import numpy as np
import cv2

cap = cv2.VideoCapture(0)
 
while(True):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('frame', frame)
    cv2.imshow('gray', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()