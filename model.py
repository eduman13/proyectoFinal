from __future__ import print_function
import pandas as pd
import os
import cv2 as cv
import numpy as np
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import commons as c
import matplotlib.pyplot as plt
from PIL import Image

def readImages(dir):
    imagenes = [cv.imread(f"{path}/{dir}/{i}.jpg", 0).flatten() for i in range(1, 121)]
    df = pd.DataFrame(imagenes)
    return df.T

path = "./data"
imagenes = []
df0 = pd.DataFrame()
df1 = pd.DataFrame()
df2 = pd.DataFrame()
df3 = pd.DataFrame()
df4 = pd.DataFrame()
for dir in os.listdir(path):
    if "0" in dir:
        df0 = df0.append(readImages(dir))
    if "1" in dir:
        df1 = df1.append(readImages(dir))
    if "2" in dir:
        df2 = df2.append(readImages(dir))
    if "3" in dir:
        df3 = df3.append(readImages(dir))
    if "4" in dir:
        df4 = df4.append(readImages(dir))
img_cols = 125
img_rows = 15
num_0 = df0.values.shape[1]
num_1 = df1.values.shape[1]
num_2 = df2.values.shape[1]
num_3 = df3.values.shape[1]
num_4 = df4.values.shape[1]
zero = df0.values.reshape((img_rows, img_cols, num_0))
one = df1.values.reshape((img_rows, img_cols, num_1))
two = df2.values.reshape((img_rows, img_cols, num_2))
three = df3.values.reshape((img_rows, img_cols, num_3))
four = df4.values.reshape((img_rows, img_cols, num_4))
X = np.concatenate((zero, one, two, three, four), axis=2).swapaxes(2,0)
y = np.concatenate((np.zeros(num_0), np.ones(num_1), np.full(num_2, 2).astype("float64"), np.full(num_3, 3).astype("float64"), np.full(num_4, 4).astype("float64")))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

num_classes = 5

# Ask keras which format to use depending on used backend and arrange data as expected
if K.image_data_format() == 'channels_first':
    X_train = X_train.reshape(X_train.shape[0], 1, img_rows, img_cols)
    X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 1)
    X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

# Incoming data is in uint8. Cast the input data images to be floats in range [0.0-1.0]
X_train = X_train.astype('float32') / 255
X_test = X_test.astype('float32') / 255

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)
print(input_shape)

## This is the neural network proposed architecture
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss="categorical_crossentropy",
              optimizer="adam",
              metrics=['accuracy'])

# Fit the NN
batch_size = 10
epochs = 10

model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_split=0.3)

# Evaluate the model with test data
score = model.evaluate(X_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

img = X_test[0]
imagenes = cv.imread("./rows/162.jpg", 0)
imagenes = imagenes.reshape(15, 125, 1)
pred = model.predict(np.expand_dims(img, axis=0))[0]
print("Probs -> zero:{0:.5f}, one:{1:.5f}, two:{2:.5f}, three:{3:.5f}, four:{4:.5f}".format(pred[0], pred[1], pred[2], pred[3], pred[4]))
predicciones = pred.tolist()
print(f"{predicciones.index(max(predicciones))}")
plt.imshow(Image.fromarray(img.squeeze()*255),'gray')
model.save("model.h5")






