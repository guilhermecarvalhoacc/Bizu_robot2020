# ENCONTRA CENTRO DE UM CORTORNO:

# exemplo contorno: 
# contornos, arvore = cv2.findContours(segmentado.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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


# ENCONTRA CENTRO DO CONTORNO DE MAIOR AREA:
def acha_centro_maior_contorno(gray):
    """ Estamos trabalhando com BGR como cores
        Retorna uma imagem com os contornos desenhados e a coordenada do centro do maior contorno
    """
    contornos, arvore = cv2.findContours(gray.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(bgr, contornos, -1, [255, 0, 0], 1)
    
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
        cv2.drawContours(bgr, [maior], -1, [0, 0, 255], 2)
        crosshair(bgr, p, 5, (0,255,0))
    
    return p


# Função que percorre a imagem e identifica as extremidades do contorno
# i = linha
# j = coluna 

def check_levels(imagem_gray):
    maior_i = -1
    menor_i = imagem_gray.shape[0] + 1
    menor_j = imagem_gray.shape[1] + 1
    maior_j = -1
    for i in range(imagem_gray.shape[0]):
        for j in range(imagem_gray.shape[1]):
            if imagem_gray[i][j] == 255:
                if i < menor_i:
                    menor_i = i
                if i  > maior_i:
                    maior_i = i
                if j  > maior_j:
                    maior_j = j 
                if j < menor_j:
                    menor_j = j
    return menor_i, maior_i, menor_j, maior_j 


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