import cv2
import numpy as np
from Holt import Holt
from CrossingNumber import CrossingNumber

###################

# 1. Aquisição da imagem. 0 = cinza
img = cv2.imread("../dataset/img_artigo.jpg", 0)
#img = cv2.imread("../dataset/1_1.png", 0)

# 2. Filtro da mediana
mediana = cv2.medianBlur(img, 5)

# 3. Filtro de aguçamento
filtro = np.array([[-1, -1, -1, -1, -1],
                   [-1,  2,  2,  2, -1],
                   [-1,  2,  3,  2, -1],
                   [-1,  2,  2,  2, -1],
                   [-1, -1, -1, -1, -1]])
sharp = cv2.filter2D(mediana, -1, filtro)

# 4. Threshould do Otsu
ret, otsu = cv2.threshold(sharp, 0, 255, cv2.THRESH_OTSU)

# 5. Afinamento método de Holt
holt = Holt()
holt_resultado = holt.apply(otsu)
holt_resultado = cv2.bitwise_not(holt_resultado)

# 6. Detectar cristas finais e bifurcações
crossingNumber = CrossingNumber()
crossingNumberResult = holt_resultado.copy()
endpoints, branches = crossingNumber.crossingNumber(crossingNumberResult)


for i in range(len(endpoints)):
	endpoint = endpoints[i]
	y = endpoint[0]
	x = endpoint[1]
	cv2.circle(crossingNumberResult, (x, y), 5, (0, 0, 255))

for i in range(len(branches)):
	branch = branches[i]
	y = branch[0]
	x = branch[1]
	cv2.circle(crossingNumberResult, (x, y), 5, (0, 0, 255))



# Amostra as ibagens
#cv2.imshow('img', img)
#cv2.imshow('mediana', mediana)
#cv2.imshow('sharp', sharp)
#cv2.imshow('filtro otsu', otsu)
cv2.imshow('holt', holt_resultado)
cv2.imshow('crossing number', crossingNumberResult)


cv2.waitKey(0)
cv2.destroyAllWindows()

