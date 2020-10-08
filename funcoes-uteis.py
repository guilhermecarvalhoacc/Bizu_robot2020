# DESENHA CENTRO:
def crosshair(img, point, size, color):
    """ Desenha um crosshair centrado no point.
        point deve ser uma tupla (x,y)
        color é uma tupla R,G,B uint8
    """
    x,y = point
    cv2.line(img,(x - size,y),(x + size,y),color,2)
    cv2.line(img,(x,y - size),(x, y + size),color,2)


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
def acha_maior_contorno_centro(gray):
    """ Estamos trabalhando com BGR como cores
        Retorna uma imagem com os contornos desenhados e a coordenada do centro do maior contorno
    """
    contornos, arvore = cv2.findContours(gray.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(bgr, contornos, -1, [255, 0, 0], 1);
    
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    
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
        cv2.drawContours(bgr, [maior], -1, [0, 0, 255], 2);
        crosshair(bgr, p, 5, (0,255,0))
    
    return bgr, p