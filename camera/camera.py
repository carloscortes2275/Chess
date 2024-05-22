import cv2

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
    
    #Aqui modificaremos cuadro para trabajar con el

class Camera:
    def __init__(self):
        self.exit = False
        self.usb = False
        
    def mostrar_video(self):
        cuadro_ancho = 57
        cuadro_alto = 42
        divisiones_x = 14
        divisiones_y = 14
        cuadros = []

        for i in range(divisiones_y):
            fila = []
            for j in range(divisiones_x):
                x1 = j * cuadro_ancho
                y1 = i * cuadro_alto
                x2 = x1 + cuadro_ancho
                y2 = y1 + cuadro_alto
                fila.append(((x1, y1), (x2, y2)))
            cuadros.append(fila)

        while True:
            ret, frame = self.cap.read()
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

            
            if self.exit:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def activar_usb(self):
        self.usb = True
        self.cap = cv2.VideoCapture(0)

    
    def activar_wifi(self,ip:str, port:int = 8080):
        self.ip = ip
        self.port = port
        self.url = f'http://{self.ip}:{self.port}/video'
        self.cap = cv2.VideoCapture(self.url)
        self.usb = False


    def cerrar(self):
        self.exit = True
 
