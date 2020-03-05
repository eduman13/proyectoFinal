import cv2 as cv
from skimage import exposure

def white_balance(img):
    white_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    white_img = exposure.rescale_intensity(white_img, out_range=(0, 255))
    return white_img