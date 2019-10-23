#! /usr/bin/env python

###############################################################################
# aruco_basic_tracking.py
#
# script testing basic tracking of Aruco markers
#
# Code modified from that at:
#  http://www.philipzucker.com/aruco-in-opencv/
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 10/21/19
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
#
# TODO:
#   * 
###############################################################################

import numpy as np
import matplotlib.pyplot as plt

import cv2
import cv2.aruco as aruco
 
# We'll do video capture on the webcam
cap = cv2.VideoCapture(0)
 
while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
 
    # lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, 
                                                          aruco_dict, 
                                                          parameters=parameters)

    # Draw the corners and ids on the original, color image
    img = aruco.drawDetectedMarkers(img, 
                                    corners, 
                                    ids, 
                                    borderColor=(0, 0, 255, 255))


    # We'll use a "fake" camera calibration matrix for now. It might mess up the results.
    # TODO: 10/21/19 - JEV - Provide instructions for generating calibration
    # NOTE; See https://github.com/CRAWlab/camera_calibration for one way to generate
    camera_matrix = np.array([[813.18292644,   0.        , 318.76403921],
                              [  0.        , 812.39009204, 239.16050615],
                              [  0.        ,   0.        ,   1.        ]])

    dist_coeffs = np.array([[-1.01845774e-01, 3.58089018e-01, -1.67284171e-04,  
                              2.08061053e-03, 7.48716318e-02]])

    markerLength = 3.75  # TODO: 10/21/19 - JEV - correct for actual markers

    # Estimate the pose of the markers in the frame
    rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 
                                                    markerLength, 
                                                    camera_matrix, 
                                                    dist_coeffs)

    # Loop through all the markers found and draw the axes on them
    for index, ID in enumerate(ids):
        aruco.drawAxis(img, camera_matrix, dist_coeffs, 
                       rvec[index], tvec[index], 0.5)
    
    # Display the resulting frame
    cv2.imshow('frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()