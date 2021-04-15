#!/usr/bin/python
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import numpy as np

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())

# Arquivos necessáriosbounding_box(maior_contorno_verde, seg_verde)
# Baixe e salve na mesma pasta que este arquivo
# https://github.com/Insper/robot20/raw/master/media/animais_caixas.mp4
video = "animais_caixas.mp4"


# Classes da MobileNet
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor"]

# Detectar
CONFIDENCE = 0.7
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))


def load_mobilenet():
    """Não mude ou renomeie esta função
        Carrega o modelo e os parametros da MobileNet. Retorna a classe da rede.
    """

    model = "MobileNetSSD_deploy.caffemodel"
    proto = "MobileNetSSD_deploy.prototxt.txt"

    net = cv2.dnn.readNetFromCaffe(proto, model) 

    return net


def detect(net, frame, CONFIDENCE, COLORS, CLASSES):
    """
        Recebe - uma imagem colorida BGR
        Devolve: objeto encontrado
    """
    img = frame.copy()
    (h, w) = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    
    # print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()

    results = []

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence


        if confidence > CONFIDENCE:
            # extract the index of the class label from the `detections`,
            # then compute the (x, y)-coordinates of the bounding box for
            # the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # display the prediction
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            # print("[INFO] {}".format(label))
            cv2.rectangle(img, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(img, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

            results.append((CLASSES[idx], confidence*100, (startX, startY),(endX, endY) ))

    return img, results


def segmenta_cor(frame, menor, maior):
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(frame_hsv,menor, maior)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(6,6))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    return mask


def acha_limites(mask):
    lin,col = np.where(mask == 255)

    i_min = min(lin)
    i_max = max(lin)
    j_min = min(col)
    j_max = max(col)
 
    #p_min = (j_min, i_min)
    #p_max = (j_max, i_max)

    return [j_min, i_min, j_max, i_max]


def calcula_iou(boxA, boxB):
    """Não mude ou renomeie esta função
        Calcula o valor do "Intersection over Union" para saber se as caixa se encontram
    """
    # https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
    # return the intersection over union value
    
    return iou


def separa_caixas(resultados):
    dog = []
    cat = []
    
    for r in resultados:
        if r[0] == "dog":
            dog.append(r)
        if r[0] == 'cat':
            cat.append(r)

    try:
        dog_rectangle = [dog[0][2][0], dog[0][2][1], dog[0][3][0], dog[0][3][1]]
        cat_rectangle = [cat[0][2][0], cat[0][2][1], cat[0][3][0], cat[0][3][1]]

        return dog_rectangle, cat_rectangle
    except:
        return None, None


if __name__ == "__main__":

    # Inicializa a aquisição da webcam
    cap = cv2.VideoCapture(video)
    cap.set(cv2.CAP_PROP_FPS, 3)


    print("Se a janela com a imagem não aparecer em primeiro plano dê Alt-Tab")

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if ret == False:
            #print("Codigo de retorno FALSO - problema para capturar o frame")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
            #sys.exit(0)

        net = load_mobilenet()
        saida, reultados = detect(net, frame.copy(), CONFIDENCE, COLORS, CLASSES)

        # Our operations on the frame come here
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        menor_azul = np.array([93, 165, 122])
        maior_azul = np.array([179, 255, 255])
        menor_verde = np.array([66, 255, 0])
        maior_verde = np.array([116, 255, 255])

        seg_azul = segmenta_cor(frame, menor_azul, maior_azul)
        seg_verde = segmenta_cor(frame, menor_verde, maior_verde)
        retangulo_azul = acha_limites(seg_azul)
        retangulo_verde = acha_limites(seg_verde)

        x1, y1, x2, y2 = retangulo_azul
        x3, y3, x4, y4 = retangulo_verde
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 3)
        cv2.rectangle(frame, (x3, y3), (x4, y4), (0,255,0), 3)

        # Checar se o cachorro está no quadrado verde:
        dog_frame, cat_frame = separa_caixas(reultados)

        if dog_frame != None:
            iou = calcula_iou(dog_frame, retangulo_verde)
            print(f"IOU: {iou}")
            if iou > 0.08:
                cv2.putText(frame, "Cachorro na caixa verde", (50, 500), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 1)
            else:
                cv2.putText(frame, "Cachorro fora da caixa verde", (50, 500), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)


        # NOTE que em testes a OpenCV 4.0 requereu frames em BGR para o cv2.imshow
        cv2.imshow('imagem', frame)
        cv2.imshow('net', saida)

        if cv2.waitKey(50) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()