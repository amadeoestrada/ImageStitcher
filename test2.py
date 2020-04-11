#!/usr/bin/env python

"""
--h for help
"""
__author__  = "Amadeo Estrada"
__date__    = "08/04/2020"

import numpy as np
import cv2
#import glob
#import sys
#import argparse

# --------------------- Set the parameters

workingFolder   = "/home/pi/Projects/ImageSticher/Images"
#imageType       = 'jpg'

#----------------------------------------- HelpFormatter

#-----------------------------------------

# Read the image file
filename = workingFolder + "/dos01.jpg"
img = cv2.imread(filename)
#cv2.imwrite(workingFolder + "/imagen_sin_distorsion.png", img)
h,  w = img.shape[:2]
print(h,w)

# # Read the camera intrinsic parameters file
# filename = workingFolder + "/cameraMatrix.txt"
# text_file = open(filename)
# mtx = text_file.readlines()
# text_file.close()
# print(mtx)
#

# Read the camera distorion file
filename = workingFolder + "/cameraDistortion.txt"
dist = np.loadtxt(filename, dtype='float', delimiter=',')
print(dist)

# Read the camera intrinsic parameters file
filename = workingFolder + "/cameraMatrix.txt"
mtx = np.loadtxt(filename, dtype='float', delimiter=',')
print(mtx)
K = np.array(mtx)
print(K)

# Get the camera matrix
newcameramtx, roi =cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),0)

print(newcameramtx)
print(roi)

# undistort
mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)

# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
print("ROI: ", x, y, w, h)

# save the image as "imagen_sin_distorsion.png"
cv2.imwrite(workingFolder + "/holoa.jpg",dst)