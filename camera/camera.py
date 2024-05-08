import cv2

class Camera:
    def __init__(self):
        self.exit = False
        self.usb = False
        
    def mostrar_video(self):

        while True:
            _, frame = self.cap.read()
            cv2.imshow('Recibiendo transmision', frame)
            
            if self.exit:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def activar_usb(self):
        self.usb = True
        self.cap = cv2.VideoCapture(1)

    
    def activar_wifi(self,ip:str, port:int = 8080):
        self.ip = ip
        self.port = port
        self.url = f'http://{self.ip}:{self.port}/video'
        self.cap = cv2.VideoCapture(self.url)
        self.usb = False


    def cerrar(self):
        self.exit = True
 
