import imutils
import commons as c
import cv2 as cv
import numpy as np
import homography as h

def readColumns():
    for i in range(1, 6):
        img = cv.imread(f"./columns/column_{i}.jpg", 0)
        findContorno(img, i)

def findContorno(img, n_column):
    ratio = img.shape[0] / 1000.0
    image = imutils.resize(img, height=1000)
    th3 = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 3)
    cnts = cv.findContours(th3.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv.contourArea, reverse=True)[1]
    #c.rotate(image, cnts)
    #c.drawContornos(image, cnts)
    contorno = [e for i in cnts.tolist() for e in i]
    listaSuma = [sum(i) for i in contorno]
    #br
    listaBr = max(listaSuma)
    br = sorted([i for i, e in zip(contorno, listaSuma) if e == listaBr], key=lambda x: x[1])[0]

    #bl
    listaBl = [i[0] for i in contorno]
    minimoListaBl = min(listaBl)
    bl = sorted([l for l, m in zip(contorno, listaBl) if minimoListaBl == m], key=lambda x: x[1], reverse=True)[0]

    #tl
    minimoTl = min(listaSuma)
    tl = [e for i, e in zip(listaSuma, contorno) if i == minimoTl][0]
    #tr
    listaTrx = [i[0] for i in contorno if i[1] < 170]
    listaTry = [i[1] for i in contorno]
    maximoListaTrx = max(listaTrx)
    minimoListaTry = min(listaTry)
    tr = [maximoListaTrx, minimoListaTry]
    #tr = sorted([i for i, e in zip(contorno, listaTrx) if e == maximoListaTr], key=lambda x: x[1], reverse=False)[0]
    tl[1] = tr[1]

    warp = h.homography(img, screenCnt=np.array([[tl], [br], [bl], [tr]]), ratio=ratio, operation="filas")
    findRows(warp, n_column)

def findRows(img, n_column):
    th3 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 45, 1)
    cnts = cv.findContours(th3.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if n_column == 5:
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:10]
    if n_column == 4:
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:25]
    else:
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:51]
    ROIs = []
    for con in cnts:
        contorno = sorted([e for i in con.tolist() for e in i], key=lambda x: sum(x), reverse=True)
        br = (contorno[0][0], contorno[0][1])
        tl = (contorno[-1][0], contorno[-1][1])
        ROIs.append([br, tl])
    puntosOrdenados = sorted(ROIs, key=lambda x: x[0][0] + x[0][1] + x[1][0] + x[1][1])
    contador = 1 if n_column == 1 else 51 if n_column == 2 else 101 if n_column == 3 else 151 if n_column == 4 else 176
    for pts in puntosOrdenados:
        ROI = img[pts[1][1]:pts[0][1], pts[1][0]:pts[0][0]]
        if ROI.shape[0] < 60:
            ROI = cv.resize(ROI, (125, 15))
            cv.imwrite(f"./rows/{contador}.jpg", ROI)
            contador += 1
            #img[tl[1]:br[1], tl[0]:br[0]]















