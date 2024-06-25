import cv2
import tensorflow as tf
import numpy as np
import threading
import time

#cambiar por un modelo mas rapido y preciso , media de actualizacion actual es de 10s
modelo = tf.keras.models.load_model('modelv3_4.keras')

diccionario = {
    0: "AZ",
    1: "KZ",
    2: "CZ",
    3: "PZ",
    4: "QZ",
    5: "TZ",
    6: "null",
    7: "AN",
    8: "KN",
    9: "CN",
    10: "PN",
    11: "QN",
    12: "TN",
    13: "AR",
    14: "KR",
    15: "CR",
    16: "PR",
    17: "QR",
    18: "TR",
    19: "AA",
    20: "KA",
    21: "CA",
    22: "PA",
    23: "QA",
    24: "TA"
}

filas = {
    0: '14',
    1: '13',
    2: '12',
    3: '11',
    4: '10',
    5: '9',
    6: '8',
    7: '7',
    8: '6',
    9: '5',
    10: '4',
    11: '3',
    12: '2',
    13: '1'
}

columnas = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H',
    8: 'I',
    9: 'J',
    10: 'K',
    11: 'L',
    12: 'M',
    13: 'N'
}

null_positions = [0, 1, 2, 11, 12, 13]


class Camera:
    def __init__(self, fn_update):
        self.exit = False
        self.usb = False
        self.piezas = []
        self.fn_update = fn_update

    def mostrar_video(self):
        cuadro_ancho = 50  # 57
        cuadro_alto = 50  # 42
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
            self.clear_pieces()
            ret, frame = self.cap.read()
            if not ret:
                break

            # Redimensionar el frame al tamaño esperado
            frame = cv2.resize(
                frame, (cuadro_ancho * divisiones_x, cuadro_alto * divisiones_y))

            # Dibujar el grid en el frame
            self.dibujar_grid(frame, cuadros, margen=5)

            start = time.time()
            # Procesar cada cuadro del grid
            for i in range(divisiones_y):
                for j in range(divisiones_x):
                    # filtramos posiciones nulas
                    if i in null_positions and j in null_positions:
                        continue
                    self.procesar_cuadro(frame, i, j, cuadros, margen=5)

            print(
                f'Tiempo de procesamiento: {time.time() - start:.2f} segundos')

            # Llamar a la función de saludo en un hilo separado
            update_thread = threading.Thread(
                target=self.fn_update, args=(None,))
            update_thread.start()
            update_thread.join()  # Espera a que termine el saludo antes de continuar

            if self.exit:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def activar_usb(self):
        self.usb = True
        self.cap = cv2.VideoCapture(0)

    def activar_wifi(self, ip: str, port: int = 8080):
        self.ip = ip
        self.port = port
        self.url = f'http://{self.ip}:{self.port}/video'
        self.cap = cv2.VideoCapture(self.url)
        self.usb = False

    def cerrar(self):
        self.exit = True

    def dibujar_grid(self, imagen, cuadros, margen=5):
        color_linea = (255, 0, 0)
        color_cuadro = (0, 255, 0)
        grosor_linea = 1
        for fila in cuadros:
            for (x1, y1), (x2, y2) in fila:
                cv2.rectangle(imagen, (x1 + margen, y1 + margen),
                              (x2 - margen, y2 - margen), color_cuadro, grosor_linea)

        # Dibujar líneas verticales
        for i in range(1, len(cuadros[0])):
            x = cuadros[0][i][0][0]
            cv2.line(imagen, (x, 0),
                     (x, imagen.shape[0]), color_linea, grosor_linea)

        # Dibujar líneas horizontales
        for i in range(1, len(cuadros)):
            y = cuadros[i][0][0][1]
            cv2.line(imagen, (0, y),
                     (imagen.shape[1], y), color_linea, grosor_linea)

    def procesar_cuadro(self, imagen, fila, columna, cuadros, margen=5):
        (x1, y1), (x2, y2) = cuadros[fila][columna]
        x1 += margen
        y1 += margen
        x2 -= margen
        y2 -= margen
        cuadro = imagen[y1:y2, x1:x2]
        # guardamos la imagen
        # cv2.imwrite(f'./pieces/{fila}_{columna}.jpg', cuadro)
        img = cv2.resize(cuadro, (128, 128))
        img = np.expand_dims(img, axis=0)
        img = img / 255.0
        # Realizar la predicción
        prediccion = modelo.predict(img)
        # Obtener la clase predicha
        clase_predicha = np.argmax(prediccion[0])
        pred = diccionario[clase_predicha]
        self.piezas.append(
            {'id': f'{columnas[columna]}{filas[fila]}', 'img': pred})

    def get_pieces(self):
        return self.piezas

    def clear_pieces(self):
        self.piezas = []
