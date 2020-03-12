import os

path = "./data/"
currentFolder = os.getcwd()
for dir, name, files in os.walk(path):
    if files:
        if "rename" not in dir:
            contador = len(os.listdir(f"{dir}_rename")) + 1
        for i in files:
            dstFolder = dir.split("x_")[1]
            if "rename" not in dstFolder:
                os.rename(f"{currentFolder}\\data\\{dir.split('/')[-1]}\\{i}", f"{currentFolder}\\data\\x_{dstFolder}_rename\\{contador}.jpg")
                contador += 1