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

# Arquivos necessários
# Baixe e salve na mesma pasta que este arquivo
# https://github.com/Insper/robot20/raw/master/media/dados.mp4
video = "dados.mp4"


if __name__ == "__main__":

    # Inicializa a aquisição da webcam
    cap = cv2.VideoCapture(video)
    cap.set(cv2.CAP_PROP_FPS, 3)


    print("Se a janela com a imagem não aparecer em primeiro plano dê Alt-Tab")

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        kernel = np.ones((3, 3),np.uint8)

        # Our operations on the frame come here
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        hsv1, hsv2 = np.array([0,0,245], dtype=np.uint8), np.array([255,15,255], dtype=np.uint8)

        mask = cv2.inRange(hsv, hsv1, hsv2)

        mask = cv2.inRange(hsv, hsv1, hsv2)
        segmentado = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((4, 4)))
        contornos, arvore = cv2.findContours(segmentado.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if ret == False:
            #print("Codigo de retorno FALSO - problema para capturar o frame")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
            #sys.exit(0)


        # Our operations on the frame come here
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        print(len(contornos))
        # NOTE que em testes a OpenCV 4.0 requereu frames em BGR para o cv2.imshow
        cv2.putText(frame, "Numero do dado: {}".format(len(contornos)),(frame.shape[1] - 600, frame.shape[0] - 10), 
        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (200, 100, 130), 2)
        cv2.imshow('imagem', segmentado)
        cv2.imshow('imagem', frame)
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


