import cv2

class Camera:
    def __init__(self, ip, puerto=8080):
        self.ip = ip
        self.puerto = puerto
        self.url = f'http://{self.ip}:{self.puerto}/video'
        self.cap = cv2.VideoCapture(self.url)
        self.exit = False

    def mostrar_video(self):
        while True:
            _, frame = self.cap.read()
            # Mostrar el fotograma
            cv2.imshow('Recibiendo transmision', frame)
            
            if self.exit:
                break

        self.cap.release()
        cv2.destroyAllWindows()
        print("Cerrando transmision")

    def cerrar(self):
        self.exit = True
 
