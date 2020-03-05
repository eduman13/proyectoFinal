import homography as h
import cv2 as cv
import commons as c

if __name__ == "__main__":
    img = cv.imread("./img/Perspectiva2.jpg")
    imgFront = h.homography(img)
    c.showImage(imgFront)