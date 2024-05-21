from camera import Camera
import flet as ft
import pickle


class Conn_camera(ft.Row):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.txt_ip = ft.TextField(
            value=None, width=200, color="blue", disabled=self.disabled)
        self.port = ft.TextField(
            value=8080, width=200, color="blue", disabled=self.disabled)
        self.cam = Camera()
        self.title = title
        self.disabled = False
        self.is_transmitting = False

    def iniciar(self, e):
        if self.cam.usb:
            self.is_transmitting = True
            self.cam.mostrar_video()
        else:
            self.cam.activar_wifi(self.txt_ip.value, self.port.value)
            self.is_transmitting = True
            self.cam.mostrar_video()

    def cerrar(self, e):
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

    def build(self) -> ft.Column:
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
                    ft.ElevatedButton(
                        "Start", on_click=self.iniciar, bgcolor="blue", color="white"),
                    ft.ElevatedButton(
                        "Finish", on_click=self.cerrar, bgcolor="pink", color="white")
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
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.WIFI), label="WIFI"),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.USB), label="USB")
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

    def build(self) -> ft.Container:
        return self.menu


class Celda(ft.Container):
    def __init__(self, color: str, top: int, left: int) -> None:
        super().__init__()
        self.color = color
        self.width = 52.5
        self.height = 52.5
        self.border_radius = 5
        self.bgcolor = color
        self.top = top
        self.left = left

    def build(self) -> ft.Container:
        return self


class Pieza(ft.Container):
    def __init__(self, img: str, top: int, left: int) -> None:
        super().__init__()
        self.width = 52.5
        self.height = 52.5
        self.image_src = img
        self.top = top
        self.left = left

    def build(self) -> ft.Container:
        return self

class Scorevalue(ft.Container):
    def __init__(self, value: int, color: str) -> None:
        super().__init__()
        self.color = color
        self.width = 20
        self.height = 20

        self.casilla = ft.Container(
            ft.Text(value, size=20),
            bgcolor=self.color,
            width=self.width,
            height=self.height,
            border_radius=5
        )

    def build(self) -> ft.Container:
        return self.casilla


class Tablero(ft.Stack):
    def __init__(self) -> None:
        super().__init__()
        self.piezas = ft.Stack()
        with open('tablero_list.pkl', 'rb') as file:
            self.tablero_l = pickle.load(file)

        self.piezas_pos = [{"img": "alfil.png", "top": 0, "left": 50}]

        self.tablero = ft.Stack(
            [Celda(i["color"], i["top"], i["left"]) for i in self.tablero_l])

        self.piezas = ft.Stack(
            [Pieza(i["img"], i["top"], i["left"]) for i in self.piezas_pos])

        self.tablero = ft.Stack(
            [
                self.tablero,
                self.piezas
            ]
        )

    def update_pos(self, positions: list):
        new_pos = []
        for p in positions:
            for i in range(len(self.tablero_l)):
                if p["id"] == self.tablero_l[i]["id"]:
                    top = self.tablero_l[i]["top"]
                    left = self.tablero_l[i]["left"]
                    img = "../sources/" + p["img"] + ".png"
                    break
            new_pos.append({"img": img, "top": top, "left": left})

        self.piezas.controls = [
            Pieza(i["img"], i["top"], i["left"]) for i in new_pos]
        self.update()

    def build(self) -> ft.Stack:
        return self.tablero


class Scores(ft.Column):
    def __init__(self) -> None:
        super().__init__()
        self.scores = {"Z": 0, "A": 0, "N": 0, "R": 0}
        self.s_blue = ft.Text(
            f" blue player        | {self.scores['Z']}", size="20", color="white", weight=ft.FontWeight.W_500)
        self.s_yellow = ft.Text(
            f" yellow player     | {self.scores['A']}", size="20", color="white", weight=ft.FontWeight.W_500)
        self.s_black = ft.Text(
            f" black player       | {self.scores['N']}", size="20", color="white",     weight=ft.FontWeight.W_500)
        self.s_red = ft.Text(
            f" red player          | {self.scores['R']}", size="20", color="white", weight=ft.FontWeight.W_500)
        self.board_scores = ft.Column(
            controls=[
                ft.Text("score", size=50, weight=ft.FontWeight.W_600,
                        font_family="BigBlueTerm437 Nerd Font"),
                ft.Row(
                    [
                        ft.Container(
                            content=self.s_blue,
                            bgcolor="blue",
                            width=200,
                            height=30,
                            border_radius=5
                        )
                    ]
                ),
                ft.Row(
                    [
                        ft.Container(
                            content=self.s_yellow,
                            bgcolor="yellow",
                            width=200,
                            height=30,
                            border_radius=5
                        )
                    ]
                ),
                ft.Row(
                    [
                        ft.Container(
                            content=self.s_black,
                            bgcolor="black",
                            width=200,
                            height=30,
                            border_radius=5
                        )
                    ]
                ),
                ft.Row(
                    [
                        ft.Container(
                            content=self.s_red,
                            bgcolor="red",
                            width=200,
                            height=30,
                            border_radius=5
                        )
                    ]
                )
            ]
        )

    def build(self) -> ft.Column:
        return self.board_scores

    def update_scores(self, positions: list):
        self.scores = self.calculate_scores(positions)
        self.s_blue.value = f" blue player        | {self.scores['Z']}"
        self.s_yellow.value = f" yellow player     | {self.scores['A']}"
        self.s_black.value = f" black player       | {self.scores['N']}"
        self.s_red.value = f" red player          | {self.scores['R']}"
        self.update()

    def calculate_scores(self, positions: list):
        PIECE_SCORES = {
            "P": 1,
            "C": 3,
            "A": 3,
            "T": 5,
            "Q": 9,
            "K": 0  # El rey no tiene puntuación porque no se cuenta en el valor del juego
        }

        scores = {
            "Z": 0,
            "A": 0,
            "N": 0,
            "R": 0
        }

        for pieza in positions:
            img_parts = pieza['img']
            piece_name = img_parts[0]  # Primera letra para identificar pieza
            piece_color = img_parts[1]  # Segunda letra para identificar color
            # Depuración
            if piece_name in PIECE_SCORES:
                scores[piece_color] += PIECE_SCORES[piece_name]
        return scores
