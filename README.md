# ImageStitcher

The code contained in image_stitcher.py uses homography to stitch two images together. First, ORB algorithm is used to 
extract the keypoints of two images. Then, using the results of ORB, the program calculates the homography matrix using 
RANSAC. The homography matrix is used to warp the second image to match the perspective on the first image to produce a 
panoramic image. 

Please note that, for this program to work, bearing in mind the final result (panoramic image), it is important that 
the first image is the one at the left. Therefore the  second image must then be the one at the right. 

The programa image_stitcher.py produces six outputs:
 1. A stitched screen image made of image 1 and image 2.
 2. A screen image made from the addition of image 1 and image 2.
 3. A stitched screen image with a blue frame that shows the homography warping of the second image.
 4, 5, 6. All previously mentioned screen images are save to disk.

---------------- ---------------- ---------------- ---------------- ---------------- ---------------- ---------------- 
Acknoledgements:
cameracalib.py and save_snaps.py are programs written by Tiziano Fiorenzani in 01/06/2018. Those programs are included 
here to help people starting with python and image analisis. 

Please visit Tiziano's sites for more interesting information: 

https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html#calibration

https://github.com/tizianofiorenzani/how_do_drones_work
