import homography as h
import cv2 as cv
import white_balance as white
import commons as c
import contours
import rows
import answer as a
import plantilla as pla

if __name__ == "__main__":
    img = cv.imread("./img/Perspectiva4.jpg")
    imgFront = h.homography(img)
    white_img = white.white_balance(imgFront)
    white_img = cv.resize(white_img, (2000, 3000))
    contours.findColumns(white_img)
    rows.readColumns()
    solutions = a.answer()
    plantilla = pla.plantilla()
    for i in range(1, 186):
        answerUser = solutions.get(str(i))
        answerReal = plantilla.get(str(i))
        print(f"Pregunta {i}: {'Acierto' if answerUser == answerReal else 'Fallo'}")


