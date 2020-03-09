import homography as h
import cv2 as cv
import white_balance as white
import commons as c
import contours
import rows
import answer as a

if __name__ == "__main__":
    img = cv.imread("./img/Dataset1.jpg")
    imgFront = h.homography(img)
    white_img = white.white_balance(imgFront)
    white_img = cv.resize(white_img, (2000, 3000))
    contours.findColumns(white_img)
    rows.readColumns()
    a.readRows()
