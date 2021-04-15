# SHAPE:
"""
Informa a linha, depois a coluna:
ex- img.shape[0] = linha
    img.shape[1] = coluna 
"""

# CORTE IMAGEM:
"""
Para cortar uma imagem, basta informar as coordenadas do ponto superior esquerdo (x1, y1),
e do ponto inferior direito (x2, y2), da seguinte maneira.:

corte = img[y1:y2, x1:x2]

height, width, channels = img.shape
superior = img[0:int(height/2), 0:width]
inferior = img[int(height/2):height, 0:width]
matede_esquerda = img[0:height, 0:int(width/2)]
metade_direita = img[0:height, int(width/2):width]
"""