import numpy as np
import cv2
import time as t
import copy


def ordenar(x): # Per ordenar els arucos amb ids creixents
    return x[1][0]

def get_examen(frame): # Retorna una imatge que és l'espai delimitat per els arucos escalat correctament. La forma que te és la de un full A4. Si no detecta 4 arucos retorna 0

    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    parameters =  cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)

    if len(markerCorners) != 4:
        #print("Arucos detectats: ", len(markerCorners))
        return 0

    llista_detectats = list(zip(markerCorners, markerIds))
    llista_detectats.sort(key=ordenar)


    mostrar_imatge_marcada = False
    temp = copy.deepcopy(frame)
    # Aquest loop només marca a on són els arucos amb quadrats, posa el num a cada un i marca la seva cantonada superior esquerra
    for i, tag in llista_detectats:
        if not mostrar_imatge_marcada:
            break
        for j in range(4):
            aux = i[0]
            x_ini = int(aux[(0+j)%4][0])
            x_fin = int(aux[(1+j)%4][0])
            y_ini = int(aux[(0+j)%4][1])
            y_fin = int(aux[(1+j)%4][1])
            cv2.line(frame, (x_ini, y_ini), (x_fin, y_fin), (0, 0, 255), 1)
        cv2.putText(frame, str(tag[0]), (int(aux[2][0]), int(aux[2][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        x = int(aux[0][0])
        y = int(aux[0][1])
        cv2.circle(frame, (x, y), 2, (255, 0, 50), 2)

    punts = np.float32([[0,0], [0,0], [0,0], [0,0]])
    for i in range(len(llista_detectats)):
        x, y = llista_detectats[i][0][0][(2+i)%4]
        x = float(x)
        y = float(y)
        punts[i] =[x, y]
        if mostrar_imatge_marcada:
            cv2.circle(frame, (int(punts[i][0]), int(punts[i][1])), 2, (0, 60*i, 0), 5)

    if mostrar_imatge_marcada:
        cv2.imshow("finestra", frame)
        cv2.waitKey(0)
    frame = temp

    amplada = 600
    altura = int(amplada*1.414)
    punts_convertits = np.float32([[0,0], [amplada, 0], [amplada, altura], [0, altura]])
    matrix = cv2.getPerspectiveTransform(punts, punts_convertits)


    frame = cv2.warpPerspective(frame, matrix, (amplada, altura))

    return frame


def fer_pdf(num_preguntes, nom_fitxer):

    if num_preguntes > 60:
        return 0

    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

    height = 2100
    width = 1485
    pdf = np.full((height, width), 255.0) # Crea A4 blanc

    punts = [[0,0], [width, 0], [width, height], [0, height]]

    for i in range(1, 5):

        id = i
        img_size = 140
        marker_img = cv2.aruco.generateImageMarker(aruco_dict, id, img_size)

        if i == 1:
            pdf[50:190,50:190] = marker_img
        elif i == 2:
            pdf[50:190,width-190:width-50] = marker_img
        elif i == 3:
            pdf[height-190:height-50,width-190:width-50] = marker_img
        elif i == 4:
            pdf[height-190:height-50,50:190] = marker_img

        # Aixo de moment no es fa servir. Haure de fer-ho servir si la camara distorsiona molt el full (gran angular)

        elif i == 5:
            pdf[int(height/2-140/2):int(height/2+140/2), width-190:width-50] = marker_img
        elif i == 6:
            pdf[int(height/2-140/2):int(height/2+140/2), 50:190] = marker_img


    offset = int((2100-191*2)/num_preguntes)
    if offset > 100:
        offset = 100
    if offset < int((2100-191*2)/20):
        offset = int((2100-191*2)/20)
    for i in range(num_preguntes):
        cv2.putText(pdf, str(i+1), (221+350*int(i/20), 251+offset*(i%20)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 4, cv2.LINE_AA)
        for j in range(3):
            cv2.circle(pdf, (311+100*j+350*int(i/20), 241+offset*(i%20)), 10, (0,0,0), 1)

    cv2.imwrite(nom_fitxer, pdf)

    return pdf

def mark_circles(imatge, num_preguntes):
    # INPUT: Imatge de l'examen (ja processat i en forma A4) i numero de preguntes
    # OUTPUT: Retorna una llista amb la posicó teorica de cada resposta

    height, width, _ = imatge.shape
    offset = (2100-190*2)/num_preguntes

    if offset > 100:
        offset = 100
    if offset < (2100-190*2)/20:
        offset = (2100-190*2)/20

    offset /= 1718
    for i in range(num_preguntes):
        pos_y = int(height*0.0291)+int(offset*height)*(i%20)
        pos_x = int(width*0.1088)+(width*0.3173)*int(i/20)
        for j in range(3):
            #cv2.circle(imatge, (int(pos_x+0.09067*width*j), pos_y), 15, (255, 0, 0), 2)
            yield [int(pos_x+0.09067*width*j), pos_y]

    return
