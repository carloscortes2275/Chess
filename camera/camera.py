import cv2

class Camera:
    def __init__(self):
        self.exit = False
        self.usb = False
        
    def mostrar_video(self):

        while True:
            _, frame = self.cap.read()
            cv2.imshow('Recibiendo transmision', frame)

            # Aplicar el detector de bordes Canny al fotograma
            umbral_minimo = 100
            umbral_maximo = 200
            bordes = cv2.Canny(frame, umbral_minimo, umbral_maximo) #Funcion de OpenCV para la detección de bordes
            # Convertir los bordes a color
            bordes_color = cv2.cvtColor(bordes, cv2.COLOR_GRAY2BGR)
            # Dibujar los bordes sobre el fotograma original
            frame_con_bordes = cv2.addWeighted(frame, 0.5, bordes_color, 1, 0)
            # Mostrar el fotograma con los bordes superpuestos
            cv2.imshow('Recibiendo transmision', frame_con_bordes)
            
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
 
