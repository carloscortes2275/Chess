from camera import Camera
import flet as ft

class Conn_camera(ft.Row):
    def __init__(self,title:str) -> None:
        super().__init__()
        self.txt_ip = ft.TextField(value="", width=200,color="blue")
        self.cam = None
        self.title = title

    def iniciar(self,e):
        self.cam = Camera(self.txt_ip.value)
        self.cam.mostrar_video()

    def cerrar(self,e):
        self.cam.cerrar()

    def build(self)->ft.Column:
        return ft.Column(controls=[
            ft.Text(self.title, italic=True),
            ft.Row(
            [ 
                self.txt_ip,
            ],
            alignment=ft.MainAxisAlignment.START,

            ),
            ft.Row(
            [
                ft.TextButton("Mostrar video",on_click=self.iniciar),
                ft.TextButton("Cerrar", on_click=self.cerrar),
            ],
            alignment=ft.MainAxisAlignment.START,
            ),
        ]
        )


