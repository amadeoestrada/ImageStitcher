# ImageStitcher

The code contained in image_stitcher.py uses homography to stitch two images together. Firtst, ORB is used to extract 
the keypoints of two images. Then, using the results of ORB, the program calculates the homography matrix using RANSAC.
The homography matrix is used to warp the second image to match the perspective on the first image to produce a panorama. 

For this program to work, it is important that the first image is the one at the left. The second image must then be the 
one at the right of the panorama to be produced. 

The programa image_stitcher.py produces six outputs:
 1. A stitched screen image made of image 1 and image 2.
 2. A screen image made from the addition of image 1 and image 2.
 3. A stitched screen image with a blue frame that shows the homography warping of the second image.
 4, 5, 6. All previously mentioned screen images are save to disk.
