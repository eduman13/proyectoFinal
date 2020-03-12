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
    if n_column == 5:
        findRows(img, 5)
    else:
        ratio = img.shape[0] / 1000.0
        image = imutils.resize(img, height=1000)
        th3 = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 3)
        cnts = cv.findContours(th3.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)[1]
        contorno = [e for i in cnts.tolist() for e in i]
        listaSuma = [sum(i) for i in contorno]
        #br
        listaBr = max(listaSuma)
        br = sorted([i for i, e in zip(contorno, listaSuma) if e == listaBr], key=lambda x: x[1])[0]

        #bl
        listaBlx = [i[0] for i in contorno]
        listaBly = [i[1] for i in contorno]
        minimoListaBl = min(listaBlx)
        maximoListaBl = max(listaBly)
        bl =  [minimoListaBl, maximoListaBl]

        #tl
        minimoTl = min(listaSuma)
        tl = [e for i, e in zip(listaSuma, contorno) if i == minimoTl][0]

        #tr
        if n_column == 1 or n_column == 2 or n_column == 3:
            listaTrx = [i[0] for i in contorno if i[1] < 170]
        else:
            listaTrx = [i[0] for i in contorno]

        listaTry = [i[1] for i in contorno]
        maximoListaTrx = max(listaTrx)
        minimoListaTry = min(listaTry)
        tr = [maximoListaTrx, minimoListaTry]
        tl[1] = tr[1]

        warp = h.homography(img, screenCnt=np.array([[tl], [br], [bl], [tr]]), ratio=ratio, operation="filas")
        findRows(warp, n_column)

def findRows(img, n_column):
    th3 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 45, -1 if n_column == 5 else -1)
    cnts = cv.findContours(th3.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if n_column == 5:
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:12]
    if n_column == 4:
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:30]
    else:
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:75]
    ROIs = []
    for con in cnts:
        contorno = sorted([e for i in con.tolist() for e in i], key=lambda x: sum(x), reverse=True)
        br =[ contorno[0][0], contorno[0][1]]
        tl = [contorno[-1][0], contorno[-1][1]]
        ROIs.append([br, tl])
    controlador = 1
    stop = 50 if n_column == 1 or n_column == 2 or n_column == 3 else 10 if n_column == 5 else 25
    contador = 1 if n_column == 1 else 51 if n_column == 2 else 101 if n_column == 3 else 151 if n_column == 4 else 176
    puntosOrdenados = []
    for i in ROIs:
        if i[1][0] > 70:
            puntosOrdenados.append(i)
    puntoBr = puntosOrdenados[0][0][0]
    puntoTr = puntosOrdenados[0][1][0]
    puntosOrdenados = sorted(puntosOrdenados, key=lambda x: x[0][1])
    puntos = []
    for i, pts in enumerate(puntosOrdenados):
        if i+1 == len(puntosOrdenados):
            puntos.append(pts)
            break
        if pts[0][0] != puntoBr:
            pts[0][0] = puntoBr
        if pts[1][0] != puntoTr:
            pts[1][0] = puntoTr
        if puntosOrdenados[i+1][1][1] - puntosOrdenados[i][1][1] > 65:
            puntos.append([[pts[0][0], pts[0][1] - 45], [pts[1][0], pts[1][1]]])
            puntos.append([[pts[0][0], pts[0][1]], [pts[1][0], pts[1][1] + 45]])
        else:
            if puntosOrdenados[i+1][1][1] - puntosOrdenados[i][1][1] > 0:
                puntos.append(pts)
    for pts in puntos:
        ROI = img[pts[1][1]:pts[0][1], pts[1][0]:pts[0][0]]
        if ROI.shape[0] < 60:
            ROI = cv.resize(ROI, (125, 15))
            cv.imwrite(f"./rows/{contador}.jpg", ROI)
            contador += 1
            if controlador == stop:
                break
            else:
                controlador += 1
            #c.drawContornos(img, np.array([[[pts[0][0], pts[0][1]], [pts[1][0], pts[1][1]]]]))
