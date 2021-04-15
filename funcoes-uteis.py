# ENCONTRA CENTRO DE UM CORTORNO:
import cv2
import numpy as np
from math import *


# Segmenta cor
def segmenta_cor(frame, menor, maior):
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(frame_hsv,menor, maior)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(6,6))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    return mask

# Encontra o centro de um contorno 
def center_of_contour(contorno):
    """ Retorna uma tupla (cx, cy) que desenha o centro do contorno"""
    M = cv2.moments(contorno)
    if M["m00"] > 0.001:
        # Usando a expressão do centróide definida em: https://en.wikipedia.org/wiki/Image_moment
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return (int(cX), int(cY))
    else:
        return (-1, -1)


# ENCONTRA CENTRO E ÁREA DO CONTORNO DE MAIOR AREA:
def acha_maior_contorno(gray):
    """ Estamos trabalhando com BGR como cores
        Retorna uma imagem com os contornos desenhados e a coordenada do centro do maior contorno
    """
    contornos, arvore = cv2.findContours(gray.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    cv2.drawContours(rgb, contornos, -1, [255, 0, 0], 1)
    
    p = (0,0)
    
    maior = None
    maior_area = 0
    for c in contornos:
        area = cv2.contourArea(c)
        if area > maior_area:
            maior_area = area
            maior = c

    if maior is not None:
        p = center_of_contour(maior)      
        cv2.drawContours(rgb, [maior], -1, [0, 0, 255], 2)
        crosshair(rgb, p, 5, (0,255,0))
    
    return p, maior_area, rgb


# Função que percorre a imagem e identifica as extremidades do contorno
# i = linha
# j = coluna 

def acha_limites(mask):
    lin,col = np.where(mask == 255)

    i_min = min(lin)
    i_max = max(lin)
    j_min = min(col)
    j_max = max(col)
 
    p_min = (j_min, i_min)
    p_max = (j_max, i_max)


    return p_min, p_max


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


def identifica_maior_linha(mask):
    minLineLength = 100
    maxLineGap = 10

    lines = cv2.HoughLinesP(mask,1,np.pi/180,100,minLineLength,maxLineGap)

    maior_comprimento = 0
    maior_linha = None
    for x1,y1,x2,y2 in lines[0]:
        dist = sqrt((x1-x2)**2+(y1-y2)**2)

        if dist > maior_comprimento:
            maior_comprimento = dist
            maior_linha = [(x1,y1),(x2,y2)]
    
    return maior_linha