from camera import Camera
import flet as ft

class Conn_camera(ft.Row):
    def __init__(self,title:str) -> None:
        super().__init__()
        self.txt_ip = ft.TextField(value=None, width=200,color="blue",disabled=self.disabled)
        self.port = ft.TextField(value=8080, width=200,color="blue",disabled=self.disabled)
        self.cam = Camera()
        self.title = title
        self.disabled = False
        self.is_transmitting = False

    def iniciar(self,e):
        if self.cam.usb:
            self.is_transmitting = True
            self.cam.mostrar_video()
        else:
            self.cam.activar_wifi(self.txt_ip.value,self.port.value)
            self.is_transmitting = True
            self.cam.mostrar_video()

    def cerrar(self,e):
        if self.is_transmitting:
            self.cam.cerrar()
            self.is_transmitting = False
            print("Transmision cerrada")

    def usb_active(self):
        self.cam.activar_usb()
        self.txt_ip.disabled = True
        self.txt_ip.value = ""
        self.port.disabled = True
        self.txt_ip.label = "Is not necessary"
        self.port.value = "Is not necessary"
        self.port.color = ft.colors.GREY_400

    def wifi_active(self):
        self.txt_ip.disabled = False
        self.port.disabled = False
        self.txt_ip.label = ""
        self.port.value = 8080

    def build(self)->ft.Column:
        return ft.Column(controls=[
            ft.Text(self.title, weight=ft.FontWeight.W_500),
            ft.Row(
            [ 
                self.txt_ip,
            ]),
            ft.Row(
            [ 
                self.port,
            ]
            ),
            ft.Row(
            [
                ft.ElevatedButton("Start", on_click=self.iniciar,bgcolor="blue", color="white"),
                ft.ElevatedButton("Finish", on_click=self.cerrar,bgcolor="pink", color="white")
            ])
        ])

class Menu(ft.Row):
    def __init__(self) -> None:
        super().__init__()
        self.text = ft.Text("Menu")
        self.connection = Conn_camera("IP adress :")
        self.rail = ft.NavigationRail(
            selected_index=0,
            width=50,
            label_type=ft.NavigationRailLabelType.ALL,
            min_extended_width=400,
            height=700,
            bgcolor=ft.colors.GREY_100,
            destinations=[
                ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.WIFI), label="WIFI"),
                ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.USB), label="USB")
            ],
            on_change=lambda e: self.selection_changed(e),
        )

        self.menu = ft.Row(
        [
            self.rail,
            ft.Column([self.connection]),
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
        alignment=ft.MainAxisAlignment.CENTER,
        )


    def selection_changed(self, e):
        if e.control.selected_index == 1:
            self.connection.usb_active()
        elif e.control.selected_index == 0:
            self.connection.wifi_active()
        self.update()

    def build(self)->ft.Row:
        return self.menu


    
   

