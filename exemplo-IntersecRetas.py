#!/usr/bin/python
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import numpy as np
import auxiliar as aux

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())

# Arquivos necessários
video = "lines.mp4"


def mensagem_falta_arquivos():
    msg = """ls
    ls

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


def encontra_reta(img, codigo_cor):
    hsv_1, hsv_2 = aux.ranges(codigo_cor)

    # convert the image to grayscale, blur it, and detect edges
    hsv = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)
    
    color_mask = cv2.inRange(hsv, hsv_1, hsv_2)
   
    segmentado = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, np.ones((10, 10)))
    
    segmentado = cv2.adaptiveThreshold(segmentado,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                 cv2.THRESH_BINARY,11,3.5)

    imagem = cv2.bitwise_not(segmentado.copy())
    
    lines = cv2.HoughLinesP(imagem, 1, np.pi/180, 30, maxLineGap=200)
    
    x1, y1, x2, y2 = lines[0][0]
    
    return x1, y1, x2, y2


def desenha_intersec(reta1, reta2, img):
    x1_1, y1_1, x2_1, y2_1 = reta1
    m_1 = ((y1_1 - y2_1)*1.0)/(x1_1 - x2_1)

    x1_2, y1_2, x2_2, y2_2 = reta2
    m_2 = ((y1_2 - y2_2)*1.0)/(x1_2 - x2_2)

    # Intersecção 
    x = ((y1_1 - y1_2 + m_2*x1_2 - m_1*x1_1)*1.0)/(m_2 - m_1)
    y =  m_2*x + y1_2 - m_2*x1_2

    return cv2.circle(img, (int(x), int(y)), 4, (255, 255, 255), 6)


if __name__ == "__main__":


    # Checando se os arquivos necessários existem

    # Inicializa a aquisição da webcam
    cap = cv2.VideoCapture(video)

    print("Se a janela com a imagem não aparecer em primeiro plano dê Alt-Tab")


    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret == False:
            #print("Codigo de retorno FALSO - problema para capturar o frame")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
            #sys.exit(0)

        reta_azul = encontra_reta(frame, "#0000FF")
        reta_verde = encontra_reta(frame, "#00FF00")
        reta_vermelha = encontra_reta(frame, "#FF0000")

        desenha_intersec(reta_azul, reta_verde, frame)
        desenha_intersec(reta_azul, reta_vermelha, frame)
        desenha_intersec(reta_verde, reta_vermelha, frame)

        cv2.imshow('imagem', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


