'''import cv2
import numpy as np

import ctypes
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
pantallaLargo, pantallaAncho = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
print(pantallaLargo, pantallaAncho)

# Cargar la imagen
imagen = cv2.imread('D:/Documentos/dataset/chessboard257.jpg')
imagen = cv2.resize(imagen, (799, 590))
#imagen = cv2.resize(imagen, (pantallaLargo, pantallaAncho-40))

# Extraer alto y ancho del frame
alto, ancho, _ = imagen.shape

# Calcular los puntos de división
divisiones_x = 14
divisiones_y = 14
pasos_x = ancho // divisiones_x
pasos_y = alto // divisiones_y


# Generar colores distintos para cada celda
np.random.seed(0)  # Para reproducibilidad
colores = np.random.randint(0, 255, size=(divisiones_x, divisiones_y, 3))

# Dibujar las celdas del grid sobre la imagen
for i in range(divisiones_x):
    for j in range(divisiones_y):
        x1 = i * pasos_x
        y1 = j * pasos_y
        x2 = x1 + pasos_x
        y2 = y1 + pasos_y
        color_celda = (int(colores[i, j, 0]), int(colores[i, j, 1]), int(colores[i, j, 2]))
        cv2.rectangle(imagen, (x1, y1), (x2, y2), color_celda, -1)  # -1 rellena el rectángulo

# Dibujar las líneas del grid sobre la imagen
color_linea = (0, 0, 0)  # Color negro
grosor_linea = 2

# Dibujar las líneas del grid sobre la imagen
color_linea = (0, 255, 0)  # Color verde
grosor_linea = 2

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

# Muestra la imagen en pantalla completa
cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)  # Crea una ventana con tamaño normal
cv2.setWindowProperty('Imagen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # Establece la ventana en modo pantalla completa
cv2.imshow('Imagen', imagen)  # Muestra la imagen en la ventana

# Terminar la ejecución
cv2.waitKey(0)
cv2.destroyAllWindows()'''

import cv2

# Definir el tamaño de los cuadros (puedes modificar estos valores)
cuadro_ancho = 57
cuadro_alto = 42

# Definir el número de divisiones
divisiones_x = 14
divisiones_y = 14

# Crear una matriz para almacenar las coordenadas de cada cuadro
cuadros = []

# Generar las coordenadas de cada cuadro
for i in range(divisiones_y):
    fila = []
    for j in range(divisiones_x):
        x1 = j * cuadro_ancho
        y1 = i * cuadro_alto
        x2 = x1 + cuadro_ancho
        y2 = y1 + cuadro_alto
        fila.append(((x1, y1), (x2, y2)))
    cuadros.append(fila)

# Función para dibujar el grid
def dibujar_grid(imagen, cuadros, margen=5):
    color_linea = (0, 255, 0)  # Color verde
    grosor_linea = 2
    for fila in cuadros:
        for (x1, y1), (x2, y2) in fila:
            cv2.rectangle(imagen, (x1 + margen, y1 + margen), (x2 - margen, y2 - margen), color_linea, grosor_linea)

    # Dibujar líneas verticales
    for i in range(1, len(cuadros[0])):
        x = cuadros[0][i][0][0]
        cv2.line(imagen, (x, 0), (x, imagen.shape[0]), color_linea, grosor_linea)

    # Dibujar líneas horizontales
    for i in range(1, len(cuadros)):
        y = cuadros[i][0][0][1]
        cv2.line(imagen, (0, y), (imagen.shape[1], y), color_linea, grosor_linea)

# Función para procesar y resaltar un cuadro específico con un margen
def procesar_cuadro(imagen, fila, columna, cuadros, margen=5):
    (x1, y1), (x2, y2) = cuadros[fila][columna]
    x1 += margen
    y1 += margen
    x2 -= margen
    y2 -= margen
    cuadro = imagen[y1:y2, x1:x2]
    
    # Aquí puedes aplicar cualquier técnica de visión computacional a "cuadro"
    # Por ejemplo, simplemente coloreamos el cuadro de un color diferente para resaltarlo
    #color_resaltado = (0, 0, 0)  # Rojo
    #cv2.rectangle(imagen, (x1, y1), (x2, y2), color_resaltado, -1)

# Capturar video desde la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Redimensionar el frame al tamaño esperado
    frame = cv2.resize(frame, (cuadro_ancho * divisiones_x, cuadro_alto * divisiones_y))

    # Dibujar el grid en el frame
    dibujar_grid(frame, cuadros, margen=5)

    # Procesar cada cuadro del grid
    for i in range(divisiones_y):
        for j in range(divisiones_x):
            procesar_cuadro(frame, i, j, cuadros, margen=5)

    # Mostrar el frame procesado
    cv2.imshow('Video con Grid', frame)

    # Terminar la ejecución si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar el objeto de captura y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
