#!/usr/bin/env python3

"""
April 09, 2020:
This program uses homography to stitch two images together. It uses ORB to extract the keypoints of two images, finds
the homography matrix, and uses it to warp the second image to match the perspective on the first image.

It produces six outputs:
    - A stitched screen image made of image 1 and image 2.
    - A screen image made from the addition of image 1 and image 2.
    - A stitched screen image with a blue frame that shows the homography warping of the second image.
    - All previously mentioned screen images are save to disk.
"""
__author__ = "Amadeo Estrada"
__date__ = "09/04/2020"

import numpy as np
import cv2
import copy

# Define the working folder
workingFolder = "./Images/"

# Define output image number
img_number = 1

# Define alpha for image addition
alpha = 0.5

# Define the minimum matches to proceed with homography
MIN_MATCH_COUNT = 10

# Import two images.
# NOTE 1: must be calibrated images!
# NOTE 2: The first image MUST BE the one at the right
filename = workingFolder + "u_dos01.jpg"
img1 = cv2.imread(filename)  # LEFT image
filename = workingFolder + "u_dos02.jpg"
img2 = cv2.imread(filename)  # RIGHT image

# Initiate ORB detector
orb = cv2.ORB_create()

# Find the keypoints and descriptors for both images.
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors.
matches = bf.match(des1, des2)

# Sort them in the order of their DISTANCE on x.
matches = sorted(matches, key=lambda x: x.distance)

# Store all the first 10 good matches based on their distance
good = matches[:10]

# Calculate the homography only if 10 good matches had been found
if len(good) >= MIN_MATCH_COUNT:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good])
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good])

    # Use RANSAC with threshold 10 for better results. The output is the homography matrix H and a mask
    H, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 10.0)

    # Calculate the new image horizontal size
    # The vertical maximum will always be the bottom of the first image
    h_size1 = np.matmul(H, np.array([[img2.shape[1]], [0], [1]]))
    result1 = h_size1 // h_size1[2][0]
    h_size2 = np.matmul(H, np.array([[img2.shape[1]], [img2.shape[0]], [1]]))
    result2 = h_size2 // h_size2[2][0]
    if result1[0][0] >= result2[0][0]:
        h_max = int(result1[0][0]) - 1
    else:
        h_max = int(result2[0][0]) - 1

    # Build perspective up to twice the horizontal size
    # w_image stands for warped image
    w_image = cv2.warpPerspective(img2, H, (h_max, img2.shape[0]), flags=cv2.INTER_LINEAR)

    # Make a copy of the warped image
    stitch_image = copy.copy(w_image)

    # Image stitching
    stitch_image[0:img1.shape[0], 0:img1.shape[1]] = img1

    # Make a copy of the warped image
    frame_image = copy.copy(stitch_image)

    # -------------------- Image addition process
    # Make image 1 the size of warped image. Fill the void with zeroes
    pic1 = np.zeros((w_image.shape[0], w_image.shape[1], 3), dtype=np.uint8)
    pic1[0:img1.shape[0], 0:img1.shape[1]] = img1

    # Image blending using addition of image 1 and warped image 2
    beta = (1.0 - alpha)
    blend_image = cv2.addWeighted(pic1, alpha, w_image, beta, 0)
    # -------------------- End of Image addition process

    # Show the warping frame
    matchesHask = mask.ravel().tolist()
    h, w, d = img1.shape
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, H)
    frame_image = cv2.polylines(frame_image, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

    # Show the images on screen
    cv2.imshow('Stitch img1 + img2', stitch_image)
    cv2.imshow('Stitch img1 + img2 + homography frame', frame_image)
    cv2.imshow('Add img1 + img2', blend_image)

    # Save the images on file
    cv2.imwrite(workingFolder + "warped_image%d.jpg" % img_number, stitch_image)
    cv2.imwrite(workingFolder + "blend_image%d.jpg" % img_number, blend_image)
    cv2.imwrite(workingFolder + "frame_image%d.jpg" % img_number, frame_image)

    # Wait for keyboard hit
    cv2.waitKey(0)

else:
    print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
    matchesMask = None
