import cv2 as cv

def showAllImage(img):
    cv.namedWindow('image', cv.WINDOW_NORMAL)
    cv.imshow("image", img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def showSmallImage(img):
    cv.imshow("image", img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def drawContornos(img, screenCnt):
    cv.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
    cv.imshow("image", img)
    cv.waitKey(0)

def drawContornosRotate(img, screenCnt):
    cv.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
    img = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
    cv.imshow("image", img)
    cv.waitKey(0)

def drawThList(img, screenCnt):
    cv.drawContours(img, screenCnt, -1, (255, 255, 255), 3)
    cv.imshow("Contour", img)
    cv.waitKey(0)