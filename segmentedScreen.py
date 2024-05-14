import cv2
import numpy as np

# Cargar la imagen
imagen = cv2.imread('D:/Documentos/dataset/chessboard257.jpg')
imagen = cv2.resize(imagen, (800, 600))

# Extraer alto y ancho del frame
alto, ancho, _ = imagen.shape

# Calcular los puntos de división
divisiones_x = 14
divisiones_y = 14
pasos_x = ancho // divisiones_x
pasos_y = alto // divisiones_y

# Dibujar las líneas del grid sobre la imagen
color_linea = (0, 255, 0)  # Color verde
grosor_linea = 1

# Líneas verticales
for i in range(1, divisiones_x):
    x = i * pasos_x
    cv2.line(imagen, (x, 0), (x, alto), color_linea, grosor_linea)

# Líneas horizontales
for i in range(1, divisiones_y):
    y = i * pasos_y
    cv2.line(imagen, (0, y), (ancho, y), color_linea, grosor_linea)

# Mostrar la imagen con el grid
cv2.imshow('Imagen con Grid', imagen)

# Terminar la ejecución
cv2.waitKey(0)
cv2.destroyAllWindows()