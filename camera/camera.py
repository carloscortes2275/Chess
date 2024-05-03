import cv2

class Camera:
    def __init__(self, ip, puerto=8080):
        self.ip = ip
        self.puerto = puerto
        self.url = f'http://{self.ip}:{self.puerto}/video'
        self.cap = cv2.VideoCapture(self.url)

    def mostrar_video(self):
        while True:
            _, frame = self.cap.read()
            # Mostrar el fotograma
            cv2.imshow('Recibiendo transmision', frame)
            
            # Salir del bucle si se presiona 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Liberar la cámara y cerrar la ventana
        self.cap.release()
        cv2.destroyAllWindows()

    




