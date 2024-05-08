import cv2

class Camera:
    def __init__(self, ip, puerto=8080):
        self.ip = ip
        self.puerto = puerto
        self.url = f'http://{self.ip}:{self.puerto}/video'
        self.cap = cv2.VideoCapture(self.url)
        self.exit = False
        self.usb = False
        
    def mostrar_video(self):
        if self.usb:
            self.cap = cv2.VideoCapture(0)
        while True:
            _, frame = self.cap.read()
            cv2.imshow('Recibiendo transmision', frame)
            
            if self.exit:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
        print("Cerrando transmision")

    def cerrar(self):
        self.exit = True
 
