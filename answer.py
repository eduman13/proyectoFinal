import cv2 as cv
import pandas as pd

def readRows():
    imagenes = [cv.imread(f"./rows/{i}.jpg") for i in range(1, 186)]
    df = pd.DataFrame(imagenes)
    print(df)

