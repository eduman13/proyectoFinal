import imutils
import commons as c
import cv2 as cv
import numpy as np
import homography as h

def readColumns():
    columns = []
    img = cv.imread(f"./columns/column_{2}.jpg", 0)
    findContorno(img)

def find(img):
    # load the query image, compute the ratio of the old height
    # to the new height, clone it, and resize it
    ratio = img.shape[0] / 1000.0
    image = imutils.resize(img, height=1000)

    # convert the image to grayscale, blur it, and find edges
    # in the image
    img = cv.medianBlur(image, 5)
    ret, th1 = cv.threshold(image, 127, 255, cv.THRESH_BINARY)
    th2 = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_MEAN_C, \
                               cv.THRESH_BINARY, 3, 2)
    th3 = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, \
                               cv.THRESH_BINARY, 11, 2)
    cnts = cv.findContours(th3.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:5]
    c.drawContornos(image, np.array([[[20, 20]], [[20, 40]], [[140, 40]], [[140, 20]]]))

def findLines(img):
    ratio = img.shape[0] / 1000.0
    image = imutils.resize(img, height=1000)
    edges = cv.Canny(image, 75, 150)
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=5)
    eje = []
    eje1 = []
    eje2 = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        eje.append((x1, y1, x2, y2))
        eje1.append(x1)
        eje2.append(y1)
        cv.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    c.showImage(image)
    xinf = min(eje1)
    yinf = max(eje2)
    xmax = max(eje1)
    print(xmax, yinf)
    print(xinf, yinf)
    suma = [i[0] + i[1] + i[2] + i[3] for i in eje]
    minimo = min(suma)
    rectaSuperior = [e for e, s in zip(eje, suma) if s == minimo]
    print("recta", rectaSuperior)
    punto1 = [rectaSuperior[0][0], rectaSuperior[0][1]]
    punto2 = [rectaSuperior[0][2], rectaSuperior[0][3]]
    x = punto1 if sum(punto1) < sum(punto2) else punto2
    print(punto2)
    c.drawContornos(image, np.array([[[143, 977]], [[14, 977]]]))
    for i in range(1, 51):
        pass
        #c.drawContornos(image, np.array([[[x[0], x[1]]], [[x[0] + 120 * i, x[1]]], [[x[0] + 120 * i, x[1] + 20 * i]], [[x[0], x[1] + 20 * i]]]))

def findContorno(img):
    ratio = img.shape[0] / 1000.0
    image = imutils.resize(img, height=1000)
    th2 = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_MEAN_C, \
                               cv.THRESH_BINARY, 7, 2)
    th3 = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, \
                               cv.THRESH_BINARY, 11, 3)
    cnts = cv.findContours(th3.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv.contourArea, reverse=True)[1]
    lista = cnts.tolist()
    lista = [e for i in lista for e in i]
    listaSuma = [sum(i) for i in lista]
    x = max(listaSuma)
    ma = sorted([i for i, e in zip(lista, listaSuma) if e == x], key=lambda x: x[1])[0]
    xs = [i[0] for i in lista]
    minimo = min(xs)
    mi = sorted([l for l, m in zip(lista, xs) if minimo == m], key=lambda x: x[1], reverse=True)[0]
    x2 = min(listaSuma)
    mas = [e for i, e in zip(listaSuma, lista) if i == x2]
    print(mas)
    x1s = [i[1] for i in lista]
    xxx = min(x1s)
    fucking = sorted([i for i, e in zip(lista, x1s) if e == xxx], key=lambda x: x[0], reverse=True)[0]
    print(fucking)
    #c.drawContornos(image, cnts)
    #c.rotate(image, cnts)
    #c.rotate(image, np.array([[fucking], [mas[0]], [mi], [ma]]))
    c.rotate(image, np.array([[mi]]))
    warp = h.homography(img, screenCnt=np.array([[mas[0]], [ma], [mi], [fucking]]), ratio=ratio, operation="maquinote")
    c.showSmallImage(warp)















