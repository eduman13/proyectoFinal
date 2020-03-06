import cv2 as cv

def showImage(img):
    cv.namedWindow('image', cv.WINDOW_NORMAL)
    cv.imshow("image", img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def drawContornos(img, screenCnt):
    cv.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
    cv.imshow("Game Boy Screen", img)
    cv.waitKey(0)

def drawTh(img, screenCnt):
    cv.drawContours(img, screenCnt, -1, (255, 255, 255), 3)
    cv.imshow("Contour", img)
    cv.waitKey(0)