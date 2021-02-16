#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
* @par Copyright (C): 2010-2020, hunan CLB Tech
* @file         45_objectDetectTrack.py
* @version      V2.0
* @details
* @par History

@author: zhulin
"""
import numpy as np
import cv2
import os
import time  
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import threading

import sys
import importlib
importlib.reload(sys)
sys.setdefaultencoding('utf8')

#初始化PCA9685和舵机
servo_pwm = Adafruit_PCA9685.PCA9685()  # 实例话舵机云台

# 设置舵机初始值，可以根据自己的要求调试
servo_pwm.set_pwm_freq(60)  # 设置频率为60HZ
servo_pwm.set_pwm(5,0,325)  # 底座舵机
servo_pwm.set_pwm(4,0,325)  # 倾斜舵机
time.sleep(1)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#初始化摄像头并设置阙值
usb_cap = cv2.VideoCapture(0)
# 设置显示的分辨率，设置为320×240 px
usb_cap.set(3, 320)
usb_cap.set(4, 240)

pid_x=0
pid_y=0
pid_w=0
pid_h=0

#舵机云台的每个自由度需要4个变量
pid_thisError_x=0   #当前误差值
pid_lastError_x=0   #上一次误差值
pid_thisError_y=0
pid_lastError_y=0

# 舵机的转动角度
pid_X_P = 330
pid_Y_P = 330   #转动角度

pid_flag=0
makerobo_facebool = False

# initialize LED GPIO
redLed = 21    # LED灯
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(redLed, GPIO.OUT)


# 机器人舵机旋转
def Robot_servo():
    while True:
        servo_pwm.set_pwm(5,0,650-pid_X_P)
        servo_pwm.set_pwm(4,0,650-pid_Y_P)


servo_tid=threading.Thread(target=Robot_servo)  # 多线程
servo_tid.setDaemon(True)
servo_tid.start()                               # 开启线程

# Start with LED off
GPIO.output(redLed, GPIO.LOW)
ledOn = False

while 1:
    ret,frame = usb_cap.read()       # 加载图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    max_face=0
    value_x=0
    # 找到人脸画矩形
    if len(faces)>0:
        (pid_x,pid_y,pid_w,pid_h) = faces[0]
        cv2.rectangle(frame,(pid_x,pid_y),(pid_x+pid_h,pid_y+pid_w),(0,255,0),2)
        result=(pid_x,pid_y,pid_w,pid_h)
        pid_x=result[0]+pid_w/2
        pid_y=result[1]+pid_h/2
        makerobo_facebool = True      

         # 误差值处理
        pid_thisError_x=pid_x-160
        pid_thisError_y=pid_y-120

        #自行对P和D两个值进行调整，检测两个值的变化对舵机稳定性的影响
        pwm_x = pid_thisError_x*5+1*(pid_thisError_x-pid_lastError_x)
        pwm_y = pid_thisError_y*5+1*(pid_thisError_y-pid_lastError_y)
        
        #迭代误差值操作
        pid_lastError_x = pid_thisError_x
        pid_lastError_y = pid_thisError_y
        
        pid_XP=pwm_x/100
        pid_YP=pwm_y/100
        
        # pid_X_P pid_Y_P 为最终PID值
        pid_X_P=pid_X_P+int(pid_XP)
        pid_Y_P=pid_Y_P+int(pid_YP)
        
        # 点亮LED灯
        GPIO.output(redLed, GPIO.HIGH)

        #限值舵机在一定的范围之内
        if pid_X_P>650:
            pid_X_P=650
        if pid_X_P<0:
            pid_X_P=0
        if pid_Y_P>650:
            pid_Y_P=650
        if pid_X_P<0:
            pid_Y_p=0

    # 如果没有检测到球，关闭LED灯
    else:
        GPIO.output(redLed, GPIO.LOW)
        
    # 显示图像
    cv2.imshow("MAKEROBO Robot", frame)
    if cv2.waitKey(1)==119:
        break
# do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff \n")
GPIO.cleanup()
cap.release()
cv2.destroyAllWindows()
