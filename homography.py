import cv2 as cv
import numpy as np
import imutils
import commons as c

def findContorno(image):
	# load the query image, compute the ratio of the old height
	# to the new height, clone it, and resize it
	ratio = image.shape[0] / 600.0
	image = imutils.resize(image, height=600)

	# convert the image to grayscale, blur it, and find edges
	# in the image
	gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
	gray = cv.bilateralFilter(gray, 6, 50, 50)
	edged = cv.Canny(gray, 100, 200)

	# find contours in the edged image, keep only the largest
	# ones, and initialize our screen contour
	cnts = cv.findContours(edged.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:5]
	screenCnt = None

	# loop over our contours
	for i in cnts:
		# approximate the contour
		peri = cv.arcLength(i, True)
		approx = cv.approxPolyDP(i, 0.02 * peri, True)
		# if our approximated contour has four points, then
		# we can assume that we have found our screen
		if len(approx) == 4:
			screenCnt = approx
			break
	return screenCnt, ratio

def homography(img):
	screenCnt, ratio = findContorno(img)
	pts = screenCnt.reshape(4, 2)
	rect = np.zeros((4, 2), dtype="float32")
	s = pts.sum(axis=1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]

	diff = np.diff(pts, axis=1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	rect *= ratio

	(br, bl, tl, tr) = rect
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

	maxWidth = max(int(widthA), int(widthB))
	maxHeight = max(int(heightA), int(heightB))

	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype="float32")

	M = cv.getPerspectiveTransform(rect, dst)
	warp = cv.warpPerspective(img, M, (maxWidth, maxHeight))
	return warp