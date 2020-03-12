from flask import request, Flask
import cv2 as cv
import numpy as np
import main

app = Flask(__name__)

@app.route("/correction", methods=["POST"])
def simulacroCorrecion():
    npimg = np.fromfile(request.files["file"], np.uint8)
    img = cv.imdecode(npimg, 1)
    exam = main.main(img)
    return {
        "Preguntas": [i for i in exam]
    }

@app.route("/ejemplo", methods=["GET"])
def conexion():
    return "Hola Mundo"

if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=False, threaded=False)

