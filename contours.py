import commons as c
import cv2 as cv
import imutils
import numpy as np
import homography as h

def findColumns(img):
    image = img.copy()
    ratio = image.shape[0] / 600.0
    image = imutils.resize(image, height=600)
    firstColumn = np.array([[[80, 95]], [[80, 585]], [[170, 585]], [[170, 95]]])
    secondColumn = np.array([[[150, 95]], [[150, 585]], [[240, 585]], [[240, 95]]])
    thirdColumn = np.array([[[220, 95]], [[310, 95]], [[310, 585]], [[220, 585]]])
    fourColumn = np.array([[[300, 95]], [[380, 95]], [[380, 350]], [[300, 350]]])
    fithColumn = np.array([[[300, 350]], [[300, 470]], [[380, 470]], [[380, 350]]])
    columns = [firstColumn, secondColumn, thirdColumn, fourColumn, fithColumn]
    for i, col in enumerate(columns):
        warp = h.homography(img, screenCnt=col, ratio=ratio, operation="columns")
        cv.imwrite(f"./columns/column_{i+1}.jpg", warp)