#!/usr/bin/python
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import argparse
import numpy as np

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())


# Arquivos necessários
model = "MobileNetSSD_deploy.caffemodel"
proto = "MobileNetSSD_deploy.prototxt.txt"
video = "dogs_chairs.mp4"


def mensagem_falta_arquivos():
    msg = """
    Tente apagar os arquivos em robot20/ros/exemplos_python/scripts:
         MobileNetSSD_deploy.prototxt.txt
         MobileNetSSD_deploy.caffemodel
    Depois
        No diretório robot20/ros/exemplos_python/scripts fazer:
        git checkout MobileNetSSD_deploy.prototxt.txt
        Depois ainda: 
        git lfs pull 

        No diretório No diretório robot20/media

        Fazer:
        git lfs pull

        Ou então baixe os arquivos manualmente nos links:
        https://github.com/Insper/robot20/tree/master/ros/exemplos_python/scripts
        e
        https://github.com/Insper/robot20/tree/master/media
    """
    print(msg)

def detect(frame):
    """
        Recebe - uma imagem colorida
        Devolve: objeto encontrado
    """
    image = frame.copy()
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    print("[INFO] computing object detections...")
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
            print("[INFO] {}".format(label))
            cv2.rectangle(image, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

            results.append((CLASSES[idx], confidence*100, (startX, startY),(endX, endY) ))

    # show the output image
    return image, results #saída, resultados

########### Funções da solução ###############

from numpy import array, uint8
yellow = [array([19,  50,  50], dtype=uint8),array([29, 255, 255], dtype=uint8) ]
magenta = [array([128,  50,  50], dtype=uint8),array([138, 255, 255], dtype=uint8)] 

def count_pixels(mask, ponto1, ponto2, txt_color):
    """ Recebe uma mascara binaria e 2 pontos e conta quantos pixels são brancos na mascara"""
    x1, y1 = ponto1
    x2, y2 = ponto2

    font = cv2.FONT_HERSHEY_SIMPLEX 
    # Selecionando só a região da imagem com o cachorro
    submask = mask[y1:y2,x1:x2]
    # Somando os pixels 255 e dividindo por 255 para saber quantos são
    pixels = np.sum(submask)/255
    # O resto é só plot
    rgb_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    cv2.rectangle(rgb_mask, ponto1, ponto2, (255,0,0), 3)
    cv2.putText(rgb_mask, "%s:%d"%(txt_color, pixels), (int((x1+x2)/2), int((y1+y2)/2)), font, 1, (0,255,0),1,cv2.LINE_AA)
    return pixels, rgb_mask
    
def plota_contagem(rgb, texto):
    cv2.imshow(texto, rgb)
    cv2.waitKey(1)
    
def classifica_cadeira(dog, chair, frame):
    """ Analisa se o dog está em cima da cadeira
        de acordo com a regra da prova. 
        Se estiver, imprime mensagem na tela *e* deixa o dog com retângulo vermelho
        Recebe: tuplas já encontradas com o dog e a chair
    """
    dog_p1 = dog[2]
    dog_p2 = dog[3]
    center_x = (dog_p1[0] + dog_p2[0])/2
    cadeira_p1 = chair[2]
    cadeira_p2 = chair[3]
    
    font = cv2.FONT_HERSHEY_SIMPLEX 

    if cadeira_p1[0] < center_x < cadeira_p2[0]: # x: Se o centro do cão estiver dentro da área da cadeira
        if min(dog_p1[1], dog_p2[1]) < max(cadeira_p1[1], cadeira_p2[1]): # y: se o cao estiver acima da cadeira:
            # Lembrem-se que na OpenCV o canto superior esq. é (0,0) e as coordenadas crescem para direita 
            # e para baixo
            cv2.putText(frame, "Cao sobre a cadeira", (50, 50), font, 1, (0, 0, 255),1,cv2.LINE_AA)
            cv2.rectangle(frame, dog_p1, dog_p2, (0,0,255), 3)
    return frame


def q1_solution(resultados, frame):
    # Variaveis de descricao da cena
    chair = None
    dogs = []
    dog_categories = ["dog", "person"]
    dog_magenta = None
    dog_yellow = None
    
    # Percorre os resultados da rede neural
    for r in resultados:
        if r[0] == "chair":
            chair = r
        if r[0] in dog_categories:
            dogs.append(r)
            
    print("dogs", dogs)
    ### Vamos classificar os cães em amarelo ou rosa, se houver
    if len(dogs)>=1:
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Máscara para filtra amarelo
        mask_yellow = cv2.inRange(frame_hsv, yellow[0], yellow[1])
        # Máscara para filtrar magenta
        mask_magenta = cv2.inRange(frame_hsv, magenta[0], magenta[1])
        for d in dogs:
            qtd_amarelo, rgb_amarelo = count_pixels(mask_yellow.copy(), d[2], d[3], "Am.")
            plota_contagem(rgb_amarelo, "Amarelo")
            qtd_magenta, rgb_magenta = count_pixels(mask_magenta.copy(), d[2], d[3], "Mag.")
            plota_contagem(rgb_magenta, "Magenta")
            if qtd_amarelo > 50: # 50 foi escolhido para rejeitar eventuais ruidos
                dog_yellow = d
            elif qtd_magenta > 50:
                dog_magenta = d
    if chair is not None:
        if dog_magenta is not None:
            classifica_cadeira(dog_magenta, chair, frame)        
        if dog_yellow is not None:
            classifica_cadeira(dog_yellow, chair, frame)


    
########## Fim das funções da solução ##########

if __name__ == "__main__":

    # Inicializa a aquisição da webcam
    cap = cv2.VideoCapture(video)

    # cria a rede neural
    net = cv2.dnn.readNetFromCaffe(proto, model)

    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor"]   

    CONFIDENCE = 0.7
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))


    print("Se a janela com a imagem não aparecer em primeiro plano dê Alt-Tab")

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if ret == False:
            #print("Codigo de retorno FALSO - problema para capturar o frame")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
            #sys.exit(0)

        # Our operations on the frame come here
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        saida, resultados = detect(frame)
        
        ### Aplicação da solução
        q1_solution(resultados, frame)

        # NOTE que em testes a OpenCV 4.0 requereu frames em BGR para o cv2.imshow
        cv2.imshow('imagem', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()