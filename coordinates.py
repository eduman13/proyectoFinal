import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

root = tk.Tk()

def get_coordinates():
    coordenates = []
    frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=tk.E + tk.W)
    yscroll = tk.Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=tk.N + tk.S)
    canvas = tk.Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=tk.BOTH, expand=1)

    # adding the image
    File = askopenfilename(parent=root, initialdir="./img", title="img")
    img = Image.open(("./img/Completa.jpg"))
    imgNumpy = np.asarray(img)
    print("imgNumpy", imgNumpy.shape)
    img = ImageTk.PhotoImage(Image.open(File))
    print(type(img))
    #print("Pillow: ", imgNumpy.shape)

    canvas.create_image(0, 0, image=img, anchor="nw")
    canvas.config(scrollregion=canvas.bbox(tk.ALL))

    # mouseclick event
    canvas.bind("<Button 1>", lambda x: get_coordinates_image(x, coordenates))

    root.mainloop()
    return coordenates

def get_coordinates_image(event, coordenates):
    coordenates.append((event.x, event.y))
    print(coordenates)
    return coordenates







