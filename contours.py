import commons as c
import cv2 as cv
import imutils
import numpy as np

def contours(image):
    # load the query image, compute the ratio of the old height
    # to the new height, clone it, and resize it
    ratio = image.shape[0] / 600.0
    image = imutils.resize(image, height=750)

    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv.bilateralFilter(image, 4, 90, 90)
    edged = cv.Canny(gray, 9, 30)

    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour
    cnts = cv.findContours(edged.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:10]
    screenCnt = None

    # loop over our contours
    for i in cnts:
        # approximate the contour
        peri = cv.arcLength(i, False)
        approx = cv.approxPolyDP(i, peri, True)
        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        screenCnt = approx
    c.showImage(edged)
    #c.drawContornos(image, screenCnt)