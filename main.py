import homography as h
import cv2 as cv
import white_balance as white
import commons as c
import contours
import rows
import answer as a
import plantilla as pla

def main(img):
    #img = cv.imread("./img/Casa.jpg")
    imgFront = h.homography(img)
    white_img = white.white_balance(imgFront)
    white_img = cv.resize(white_img, (2000, 3000))
    contours.findColumns(white_img)
    rows.readColumns()
    solutions = a.answer()
    plantilla = pla.plantilla()
    exam = []
    for i in range(1, 186):
        answerUser = solutions.get(str(i))
        answerReal = plantilla.get(str(i))
        respuestas = {
            f"Pregunta_{i}": "Acierto" if answerUser == answerReal else "Fallo",
            "Respuesta_Usuario": answerUser,
            "Respuesta_Correcta": answerReal
        }
        exam.append(respuestas)
    return exam