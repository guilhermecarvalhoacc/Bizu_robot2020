import cv2

# CHAMADA: crosshair(bgr, p, 5, (0,255,0))
def crosshair(img, point, size, color):
    """ Desenha um crosshair centrado no point.
        point deve ser uma tupla (x,y)
        color é uma tupla R,G,B uint8
    """
    x,y = point
    cv2.line(img,(x - size,y),(x + size,y),color,2)
    cv2.line(img,(x,y - size),(x, y + size),color,2)


def coloca_texto(frame, org):
    """
    cv2.putText(image, text, org, font, fontScale, color[, thickness[, 
                lineType[, bottomLeftOrigin]]])
    
    org = coordinates of the bottom-left corner of the text string in the image
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "texto", org, font, 2.0, (0, 255, 0), 3)


def desenha_contornos(frame, contorno):
    cv2.drawContours(frame, contorno, -1, (0, 255, 0), 2)


def desenha_retangulo(img, ponto1, ponto2):
    cv2.rectangle(img, ponto1, ponto2, (255,0,0), 3)


def desenha_circulos(img, center, radius, color):
    cv2.circle(img, center, radius, color, thickness=1, lineType=8, shift=0)


def desenha_linha(img, ponto1, ponto2):
    cv2.line(img, ponto1, ponto2,(0,0,255),2)