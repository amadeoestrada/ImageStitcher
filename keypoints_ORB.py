#!/usr/bin/env python3

"""
April 09, 20202:
This program opens two files called dos01.jpg and dos05.jpg. Then extracts the keypoints of both files using ORB.
"""
__author__ = "Amadeo Estrada"
__date__ = "09/04/2020"

import numpy as np
import cv2
from matplotlib import pyplot as plt

# Define the working folder
workingFolder = "./Images/"

MIN_MATCH_COUNT = 10
filename = workingFolder + "u_dos01.jpg"
img1 = cv2.imread(filename)          # queryImage
filename = workingFolder + "u_dos05.jpg"
img2 = cv2.imread(filename) # trainImage

# Initiate ORB detector
orb = cv2.ORB_create()

# # find the keypoints and descriptors with SIFT
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors.
matches = bf.match(des1,des2)

# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)

# Draw first 10 matches.
img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:10],2)

plt.imshow(cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)),plt.show()