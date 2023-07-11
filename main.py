import numpy as np
import cv2
from funcions import get_examen, fer_pdf, mark_circles
import time as t
import os
import tensorflow as tf


def guardar_exemple(coordenades, examen, count, size):
    carpeta = "no_marcat"
    if int(count/30)%2 == 0:
        carpeta = "marcat"

    fitxers = os.listdir(carpeta)

    i = coordenades

    path = str(carpeta+'/'+str(len(fitxers)+1)+".png")
    img_resposta = final[int(i[1]-size/2):int(i[1]+size/2), int(i[0]-size/2):int(i[0]+size/2)]
    cv2.imwrite(path, img_resposta)

    return count + 1


def respostes_marcades(model, final, coordenades, size):
    imatges = []
    size = 40
    for i in coordenades:
        imatges.append(final[int(i[1]-size/2):int(i[1]+size/2), int(i[0]-size/2):int(i[0]+size/2)])

    #imatges = np.expand_dims(imatges, axis=0)
    imatges = tf.data.Dataset.from_tensor_slices(imatges).batch(1)
    r = list(model.predict(imatges, verbose = 0))
    for i in range(len(r)):
        r[i] = np.argmax(r[i])


    return r




cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # this is the magic!
"""
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
"""

model = tf.keras.models.load_model("xarxa_neuronal")

buscar_respostes = False
key = ord('q')
last_key = key
while True:
    ret, vid = cap.read()


    if ret:

        cv2.imshow("video", vid)
        final = get_examen(vid)

        if (type(final) != int and buscar_respostes): # Si es detecta un examen
            result = list(mark_circles(final, 60))
            count = 0
            size = 40

            inici = t.time()

            respostes = respostes_marcades(model, final, result, size)

            for n in range(len(respostes)):
                #count = guardar_exemple(result[n], final, count) # Per guardar imatges per fer training

                i = result[n]

                cv2.rectangle(final, (int(i[0]-size/2), int(i[1]-size/2)), (int(i[0]+size/2), int(i[1]+size/2)), (0,0,255), 2)
                if not respostes[n]: # Si el model retorna 0, és a dir que és resposta marcada
                    cv2.rectangle(final, (int(i[0]-size/2), int(i[1]-size/2)), (int(i[0]+size/2), int(i[1]+size/2)), (0,255,0), 2)

            print(t.time()-inici, "segons en computar totes les instancies de la xarxa neuronal")
            t.sleep(0.25)
            cv2.imshow("examen", final)
            cv2.waitKey(0)


        elif (type(final) != int):
            cv2.imshow("examen", final)

        else:
            cv2.imshow("examen", np.zeros((848,600)))

        last_key = key
        key = cv2.waitKey(1)

        if key == ord('q'): # Si es clicka la Q es para el programa (alguna pestanya de cv2 ha de estar seleccionada)
            break
        buscar_respostes = False
        if key == ord('e') and last_key != ord('e'):
            buscar_respostes = True


cv2.destroyAllWindows()
quit()