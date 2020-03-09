import cv2 as cv
import pandas as pd
import commons as c

def readRows():
    imagenes = [cv.imread(f"./rows/{i}.jpg", 0) for i in range(1, 186)]
    print(type(imagenes[0][0]))
    df = pd.DataFrame([i[0] for i in imagenes])
    print(df)


