import cv2 as cv
import pandas as pd
import commons as c

def readRows():
    imagenes = [cv.imread(f"./rows/{i}.jpg", 0) for i in range(1, 186)]
    print(imagenes[0].shape)
    df = pd.DataFrame(imagenes)


