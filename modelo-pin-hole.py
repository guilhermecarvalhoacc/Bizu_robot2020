# Encontrar distância do objeto para a câmera
def encontra_distancia(H, h, f):
    distance = (H*f)/h
	
    return distance


# Parâmetros
KD = 30 # Know distance (cm)
H = 7.6 # Real distance between the two circle centers (cm)
h = 60.5 # Distance between the two circle centers in the screen  (pixel) 
f = (h*KD)/H #Pixel