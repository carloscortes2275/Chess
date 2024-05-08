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
        if self.cam:
            self.cam.cerrar()
            
    def build(self)->ft.Column:
        return ft.Column(controls=[
            ft.Text(self.title, italic=True),
            ft.Row(
            [ 
                self.txt_ip,
            ]),
            ft.Row(
            [
                ft.TextButton("Mostrar video",on_click=self.iniciar),
                ft.TextButton("Cerrar", on_click=self.cerrar),
            ])
        ])

class Menu(ft.Row):
    def __init__(self) -> None:
        super().__init__()
        self.text = ft.Text("Menu")
        self.rail = ft.NavigationRail(
            selected_index=0,
            width=50,
            label_type=ft.NavigationRailLabelType.ALL,
            min_extended_width=400,
            height=700,
            destinations=[
                ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.WIFI), label="Wifi"),
                ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.USB), label="Usb")
            ],
            on_change=lambda e: print("Selected destination:", e.control.selected_index),
        )

        self.menu = ft.Row(
            [
                self.rail,
            ])

    def build(self)->ft.Row:
        return self.menu


    
   

