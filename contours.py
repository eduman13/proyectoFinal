import commons as c
import cv2 as cv
import imutils
import numpy as np
import matplotlib as plt

def findColumns(img):
    ratio = img.shape[0] / 600.0
    img = imutils.resize(img, height=600)
    firstColumn = np.array([[[90, 105]], [[160, 105]], [[160, 585]], [[90, 585]]])
    secondColumn = np.array([[[160, 105]], [[230, 105]], [[230, 585]], [[160, 585]]])
    thirdColumn = np.array([[[230, 105]], [[300, 105]], [[300, 585]], [[230, 585]]])
    fourColumn = np.array([[[300, 105]], [[370, 105]], [[370, 350]], [[300, 350]]])
    fithColumn = np.array([[[300, 350]], [[370, 350]], [[370, 470]], [[300, 470]]])
    columns = [firstColumn, secondColumn, thirdColumn, fourColumn, fithColumn]
    for i, col in enumerate(columns):
        col = col.flatten()
        ROI = img[col[1]:col[5], col[0]:col[4]]
        cv.imwrite(f"./columns/column_{i+1}.png", ROI)

