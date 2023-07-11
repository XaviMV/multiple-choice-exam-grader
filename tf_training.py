import tensorflow as tf
import numpy as np
import time as t
import random
import os
import cv2

categories = ['marcat', 'no_marcat']

PATH = os.getcwd()

train_x = [] # arrays of images
train_y = [] # array of the images' labels

test_x = [] # arrays of images
test_y = [] # array of the images' labels


percentage_test_images = 10 # Percentage of the overall images that will be used only for the testing of the neural network

# Save images from each category (class1 and class2)
for categ in categories:
    nou_path = os.path.join(PATH, categ)
    count = 0
    for path_imatge in os.listdir(nou_path):
        img = cv2.imread(os.path.join(PATH, categ, path_imatge))
        if count%int(100/percentage_test_images) != 0:
            train_x.append(img)
            if (categ == categories[0]):
                train_y.append(0)
            else:
                train_y.append(1)
        else:
            test_x.append(img)
            if (categ == categories[0]):
                test_y.append(0)
            else:
                test_y.append(1)
        count += 1


print("TRAIN SAMPLES: ", len(train_x))
print("TEST SAMPLES: ", len(test_x))


train_x = np.asarray(train_x)
train_y = np.asarray(train_y)

test_x = np.asarray(test_x)
test_y = np.asarray(test_y)



model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (5,5), activation = "relu", input_shape=(40, 40, 3), padding='same'),
    tf.keras.layers.MaxPooling2D((3, 3)),
    tf.keras.layers.Conv2D(32, (3,3), activation = "relu", input_shape=(40, 40, 3), padding='same'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(16, activation = "relu"),
    tf.keras.layers.Dense(2, activation = "softmax")
    ])

model.summary()

t.sleep(1)

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(train_x, train_y, epochs=5, batch_size=4, verbose=1, shuffle=True)

model.save('xarxa_neuronal') # The model is saved so that it can be loaded with the function: tf.keras.models.load_model('/tmp/model')

print("TRAINING FINISHED, STARTING TEST:")

model.evaluate(test_x, test_y, verbose=2)

print(len(test_x)/(len(test_x)+len(train_x)))