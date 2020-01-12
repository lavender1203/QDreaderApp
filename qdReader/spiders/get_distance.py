#!/usr/bin/env python
# coding=utf-8
import cv2    
import numpy as np   
import pandas as pd 
import matplotlib.pyplot as plt  
import math

# x方向一阶导中值
def get_dx_median(dx,x,y,w,h):
    return np.median(dx[y:(y+h),x])    

# 预处理
def pre_process(img_path):         
    img = cv2.imread(img_path)     
    if img is None:
        print("invalide img.")
    #size = img.shape   #获取图片大小（长，宽，通道数）
    #img = cv2.resize(img,(size[1]*2,size[0]*2),cv2.INTER_LINEAR)
    #img = crop_right(img)

    # cv2.imshow('crop_right', img)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) 
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  # 转成灰度图像  

    dx = cv2.Sobel(img,-1,1,0,ksize=5) 
    dy = cv2.Sobel(img,-1,0,1,ksize=5)   
    h,w = img.shape[:2]   
      
    ret, binary = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY) #将灰度图像转成二值图像     
    # cv2.imshow('binary', binary)
    # cv2.waitKey(0)
    # binary = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3,7)  
    _,contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # 查找轮廓   
    #cv2.drawContours(gray,contours,-1,(255,255,255),2)    
    
    gray = np.zeros_like(img_gray) 
    cv2.drawContours(gray,contours,-1,(0,0,255),1)    
     
    gray = np.zeros_like(gray) 
    rect_area = []
    rect_arclength = []  
    cnt_infos = {}

    colors = plt.cm.Spectral(np.linspace(0, 1, len(contours)))  
    for i,cnt in enumerate(contours): 
        if cv2.contourArea(cnt) < 5000  or cv2.contourArea(cnt) > 25000:
            continue  

        x, y, w, h = cv2.boundingRect(cnt)  
        cnt_infos[i] = {'rect_area': w*h,  # 矩形面积
                        'rect_arclength': 2*(w+h), #矩形周长
                        'cnt_area':cv2.contourArea(cnt) , #轮廓面积
                        'cnt_arclength':cv2.arcLength(cnt,True) , #轮廓周长
                        'cnt':cnt , #轮廓
                        'w':w,
                        'h':h,
                        'x':x,
                        'y':y,
                        'mean':np.mean(np.min(img[y:(y+h),x:(x+w)],axis=2)), # 矩形内像素平均
                       }  
        rect_area.append(w*h)   
        rect_arclength.append(2*(w+h))  
        cv2.rectangle(img, (x, y), (x+w, y+h), colors[i], 1)  
        
    # plt.imshow(img)  
    return img,dx,cnt_infos

def crop_right(img):
    h, w = img.shape[:2]
    img = img[0:h, int(w/2):w]
    return img

def crop_left(img):                                                        
    h, w = img.shape[:2]
    img = img[0:h, 0:int(w/2)]
    return img

def qq_mark_detect(img_path):
    img,dx,cnt_infos = pre_process(img_path) 
    h,w = img.shape[:2]
    df = pd.DataFrame(cnt_infos).T 
    df.head() 
    df['dx_mean']=df.apply(lambda x : get_dx_median(dx,x['x'],x['y'],x['w'],x['h']),axis=1)    
    df['rect_ratio']= df.apply(lambda v:v['rect_arclength']/4/math.sqrt(v['rect_area']+1) ,axis = 1)  
    df['area_ratio']= df.apply(lambda v:v['rect_area']/v['cnt_area'] ,axis = 1)  
    # df.query('w>100').query('h>100').sort_values('area_ratio') 
    df['score'] = df.apply(lambda x: abs(x['rect_ratio']-1),axis=1)      
    result = df.query('x>0').query('area_ratio<2').query('rect_area>5000').query('rect_area<20000').sort_values(['mean','score','dx_mean']).head(2) 
    #print(result)
    if len(result):
        x_offset = result.x.values[0] + int(result.w.values[0]/2)
        #cv2.line(img,(x_offset,0),(x_offset,h),color=(255,0,255))
        #plt.imshow(img)  
        #plt.show()
        return x_offset
    return 0

def get_pos1(img_path):
    res = qq_mark_detect(img_path)
    return res

def find_contour(area, arc_len, a):
    # a = 78*1 要匹配的缺口边长
    padding = a * 0.18# 缺口预留18%边长的padding
    a = a - 2 * padding
    area_base = a * a # 缺口面积
    rate = 0.4# 容错率
    len = a * 4
    if area_base * (1-rate) < area < area_base * (1+rate) \
            and len * (1-rate) < arc_len < len * (1+rate):
        return True
    else:
        return False

def get_pos(img_path):
    # 图像预处理
    # 图像转化为灰度图并平滑
    # img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转成灰度图像
    # cv2.imshow('contours1', img_gray)
    # image = img_gray
    # image = cv2.blur(img_gray, (1, 1))
    # cv2.imshow('contours2', image)
    image = cv2.imread(img_path)
    width = image.shape[1]
    # 68*68 和136*136两种缺口大小
    if width > 400:
        a = 68*2
    else:
        a = 68
    thresh = 200
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    canny = cv2.Canny(blurred, thresh, thresh*2)
    img_c, contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]  # get largest five contour area
    # cv2.imshow('contours', img_c)
    # cv2.waitKey(0)
    # image = cv2.drawContours(image, contours, -1, (255, 255, 0), 1)  # img为三通道才能显示轮廓
    # cv2.imshow('img', img_c)
    for i, contour in enumerate(contours):
        M = cv2.moments(contour)
        if M['m00'] == 0:
            cx = cy = 0
        else:
            cx, cy = M['m10'] / M['m00'], M['m01'] / M['m00']  #计算轮廓质心位置
        if cx < int(width * 0.6):
            continue

        #通过轮廓的面积、周长以及大致位置进行查找 目标轮廓
        # print((cx, cy))
        area = cv2.contourArea(contour)
        arc_len = cv2.arcLength(contour, True)
        # print(area)
        # print(arc_len)
        if find_contour(area, arc_len, a):
            x, y, w, h = cv2.boundingRect(contour) # 外接矩形
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # cv2.imshow('image', image)
            return x + int(w/2)
    return 0

if __name__ == "__main__":
    img_path = "/home/xjg/work/QDreaderApp/img/gap1575986397630.7952.jpeg"
    # img_path = "/home/xjg/work/QDreaderApp/img/1575986433.3311968.png"
    # img_path = '/home/xjg/work/QDreaderApp/img/1575986403.3865292.png'
    # img_path = '/home/xjg/下载/hycdn_1_1729889101262871040_0.jpeg'

    #res = qq_mark_detect(img_path)
    #print(res.x)

    pos = get_pos(img_path)
    print(pos)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
