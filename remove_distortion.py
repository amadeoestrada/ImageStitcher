#!/usr/bin/env python

"""
April 09, 20202:
This program opens five files called dos01.jpg to dos05.jpg, removes the distortion of them and
saves the files into new files called u_dos01.jpg to u_dos02.jpg ('u' stands for unwarped.
"""
__author__ = "Amadeo Estrada"
__date__ = "08/04/2020"

import numpy as np
import cv2

# Define the working folder
workingFolder = "./Images/"

# Extract the camera matrix K from the parameters file:
filename = workingFolder + "/cameraMatrix.txt"
K = np.loadtxt(filename, dtype='float', delimiter=',')

# Extract distortion coefficients d from the parameters file:
filename = workingFolder + "/cameraDistortion.txt"
d = np.loadtxt(filename, dtype='float', delimiter=',')

# Initiate a while loop to unwarp all files.
a = 1

while a <= 5:
    # Read the image file and extract its size
    filename = workingFolder + "/dos0%d.jpg" % a
    img = cv2.imread(filename)
    h, w = img.shape[:2]

    # Generate new camera matrix from parameters
    newcameramatrix, roi = cv2.getOptimalNewCameraMatrix(K, d, (w, h), 0)

    # Generate look-up tables for remapping the camera image
    mapx, mapy = cv2.initUndistortRectifyMap(K, d, None, newcameramatrix, (w, h), 5)

    # Remap the original image to a new image
    newimg = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    # Save new image
    cv2.imwrite("./Images/u_dos0%d.jpg" % a, newimg)
    a += 1

cv2.waitKey(0)
