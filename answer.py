import cv2 as cv
import commons as c
from keras.models import load_model
import numpy as np
import os

path = "./rows"
img_cols = 125
img_rows = 15
model = load_model("model.h5")

def readRows():
    imagenes = []
    for i in os.listdir(path):
        imagenes.append(i)
    return sorted(imagenes, key=lambda x: int(x.split(".")[0]))

def readImages(imagenes):
    files = []
    for i in imagenes:
        files.append(cv.imread(f"{path}/{i}", 0).flatten())
    return files

def solution(imagenes):
    solutions = []
    for i in imagenes:
        img = i.reshape((img_rows, img_cols, 1)).swapaxes(2, 0)
        img = img.reshape(img_rows, img_cols, 1)
        img = img.astype("float32") / 255
        pred = model.predict(np.expand_dims(img, axis=0))[0].tolist()
        sol = pred.index(max(pred))
        solutions.append(sol)
    return solutions

def answer():
    imagenes = readRows()
    imagenes = readImages(imagenes)
    solutions = solution(imagenes)
    result = {f"{i+1}": sol for i, sol in enumerate(solutions)}
    return result