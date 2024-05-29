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
        self.width = 46
        self.height = 46
        self.border_radius = 5
        self.bgcolor = color
        self.top = top
        self.left = left

    def build(self) -> ft.Container:
        return self


class Position_Indicator(ft.Container):
    def __init__(self, top: int, left: int, id: str) -> None:
        super().__init__()
        self.color = "black"
        self.width = 46
        self.height = 46
        self.border_radius = 5
        self.bgcolor = ft.colors.TEAL_ACCENT_400
        self.top = top
        self.left = left
        self.content = ft.Text(id, text_align=ft.TextAlign.CENTER, size=30)

    def build(self) -> ft.Container:
        return self


class C_Player(ft.Container):
    def __init__(self, id: ft.Text) -> None:
        super().__init__()
        self.color = "white"
        self.width = 200
        self.height = 30
        self.border_radius = 10
        self.bgcolor = id.value
        self.content = id

    def build(self) -> ft.Container:
        return self


class Pieza(ft.Container):
    def __init__(self, img: str, top: int, left: int) -> None:
        super().__init__()
        self.width = 46
        self.height = 46
        self.image_src = img
        self.top = top
        self.left = left

    def build(self) -> ft.Container:
        return self


class Scorevalue(ft.Container):
    def __init__(self, color: str, text: ft.Text) -> None:
        super().__init__()
        self.color = "white"
        self.width = 250
        self.height = 30
        self.bgcolor = color
        self.border_radius = 7.5
        self.content = text

    def build(self) -> ft.Container:
        return self


class Tablero(ft.Stack):
    def __init__(self) -> None:
        super().__init__()
        self.players = ["red", "blue", "black", "yellow"]
        self.turno = 0
        self.piezas_pos = []
        self.prev_positions = []
        self.undo_positions = []
        self.undo_times = 0

        self.current_player = ft.Text(
            self.players[self.turno], size=20, color="white", weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER)

        self.piezas = ft.Stack()
        with open('tablero_list.pkl', 'rb') as file:
            self.tablero_l = pickle.load(file)

        # crear archivo serializado
        self.position_indicators = ft.Stack()
        with open('indicator_list.pkl', 'rb') as file:
            self.indicator_l = pickle.load(file)

        self.tablero = ft.Stack(
            [Celda(i["color"], i["top"], i["left"]) for i in self.tablero_l])

        self.indicators = ft.Stack(
            [Position_Indicator(i["top"], i["left"], i["id"])
             for i in self.indicator_l]
        )
        self.piezas = ft.Stack(
            [Pieza(i["img"], i["top"], i["left"]) for i in self.piezas_pos])

        self.c_player = C_Player(self.current_player)

        self.tablero = ft.Stack(
            [
                self.indicators,
                self.tablero,
                self.piezas,
                self.c_player,
                ft.Container(
                    content=ft.ElevatedButton(
                        bgcolor=ft.colors.PURPLE_400, color="white", icon="refresh", text="Undo move", on_click=self.undo_move),
                    top=0,
                    left=1000
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        bgcolor=ft.colors.PURPLE_400, color="white", icon="SWITCH_ACCESS_SHORTCUT_SHARP", text="Switch turn", on_click=self.switch_turn),
                    top=50,
                    left=0
                )
            ]
        )

    def switch_turn(self, e):
        if self.turno == 0:
            self.turno = 3
        else:
            self.turno -= 1

        self.current_player.value = self.players[self.turno]
        self.c_player.bgcolor = self.players[self.turno]
        self.update()

    def undo_move(self, e):
        if self.undo_times > 0:
            return

        self.piezas_pos = []
        for p in self.undo_positions:
            for i in range(len(self.tablero_l)):
                if p["id"] == self.tablero_l[i]["id"]:
                    top = self.tablero_l[i]["top"]
                    left = self.tablero_l[i]["left"]
                    img = "../sources/" + p["img"] + ".png"
                    break
            self.piezas_pos.append({"img": img, "top": top, "left": left})

        self.piezas.controls = [
            Pieza(i["img"], i["top"], i["left"]) for i in self.piezas_pos]

        # se actualiza el turno
        if self.turno == 0:
            self.turno = 3

        else:
            self.turno -= 1

        self.current_player.value = self.players[self.turno]
        self.c_player.bgcolor = self.players[self.turno]
        self.undo_times += 1

        self.update()

    def update_pos(self, positions: list):
        if not (self.is_different(self.prev_positions, positions)):
            return

        # si se ha movido una pieza contamos un turno
        self.turno += 1

        # al llegar a cuatro volvemos a empezar
        if self.turno == 4:
            self.turno = 0

        self.piezas_pos = []
        for p in positions:
            for i in range(len(self.tablero_l)):
                if p["id"] == self.tablero_l[i]["id"]:
                    top = self.tablero_l[i]["top"]
                    left = self.tablero_l[i]["left"]
                    img = "../sources/" + p["img"] + ".png"
                    break
            self.piezas_pos.append({"img": img, "top": top, "left": left})

        # antes de actualizar en la interfaz se verifica que todos los jugadores tengan su
        # rey en el tablero, de no ser asi , piezas_pos debe eliminar todas las piezas de ese jugador
        # para que ya no se muestren en la interfaz (o mejor solo dejamos las piezas en tablero y ya?), pero se debe asegurar de guardar su puntaje para que no se
        # vuelva 0 al no tener piezas suyas en el tablero (hacer modificaciones necesarias al codigo)

        # --aqui va--

        # --------------------------------------------------------------#

        # se actualizan las piezas en la interfaz
        self.piezas.controls = [
            Pieza(i["img"], i["top"], i["left"]) for i in self.piezas_pos]

        self.current_player.value = self.players[self.turno]
        self.c_player.bgcolor = self.players[self.turno]

        # antes de que prev se actualice se guarda en undo
        self.undo_positions = self.prev_positions

        # se reinicia el contador de deshacer
        self.undo_times = 0

        # prev se actualiza
        self.prev_positions = positions

        self.update()

    # para saber si se ha movido una pieza
    def is_different(self, prev, new):
        return prev != new

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
                        Scorevalue("blue", self.s_blue)
                    ]
                ),
                ft.Row(
                    [
                        Scorevalue("#ffc400", self.s_yellow)
                    ]
                ),
                ft.Row(
                    [
                        Scorevalue("black", self.s_black)
                    ]
                ),
                ft.Row(
                    [
                        Scorevalue("red", self.s_red)
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
