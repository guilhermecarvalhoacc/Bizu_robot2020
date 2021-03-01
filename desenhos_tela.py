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
    cv2.putText(frame, "texto", org, cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 255, 0), 3)


def desenha_contornos(frame, contorno):
    cv2.drawContours(frame, contorno, -1, (0, 255, 0), 2)