from components import *
import flet as ft
import time

tablero = Tablero()
scores = Scores()


def update(new_pos):
    tablero.update_pos(new_pos)
    scores.update_scores(new_pos)


def main(page: ft.Page):
    page.title = "AI Chess"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.START
    page.window_maximized = True
    page.scroll = True
    menu = Menu()

    # Obtener el tamaño de la pantalla
    window_width = page.window_width
    window_height = page.window_height
    print(window_width, window_height)
    # Ejemplo de las posiciones obtenidas de la IA (sirve para calcular los scores de las piezas y
    # mostrarlas las piezas en la interfaz gráfica)

    # red
    new_pos = [
        {"id": "D14", "img": "AZ"},
        {"id": "E14", "img": "PN"},
        {"id": "F13", "img": "TR"},
        {"id": "G14", "img": "QA"},
        {"id": "H14", "img": "QZ"}
    ]

    # blue
    new_pos2 = [
        {"id": "D13", "img": "AZ"},
        {"id": "E14", "img": "PN"},
        {"id": "F13", "img": "TR"},
        {"id": "G14", "img": "QA"},
        {"id": "H14", "img": "QZ"}
    ]

    # black
    new_pos3 = [
        {"id": "D13", "img": "AZ"},
        {"id": "E13", "img": "PN"},
        {"id": "F13", "img": "TR"},
        {"id": "G14", "img": "QA"},
        {"id": "H14", "img": "QZ"}
    ]

    # yellow
    new_pos4 = [
        {"id": "D13", "img": "AZ"},
        {"id": "E13", "img": "PN"},
        {"id": "F13", "img": "TR"},
        {"id": "G13", "img": "QA"},
        {"id": "H14", "img": "QZ"}
    ]

    # red
    new_pos5 = [
        {"id": "D13", "img": "AZ"},
        {"id": "E13", "img": "PN"},
        {"id": "F12", "img": "TR"},
        {"id": "G13", "img": "QA"},
        {"id": "H14", "img": "QZ"}
    ]

    page.add(ft.Row(
        [
            ft.Column(
                [
                    ft.Container(
                        content=menu,
                        bgcolor=ft.colors.GREY_100,
                        padding=20,
                        width=window_width * 0.23,
                        border_radius=10,
                        height=window_height*0.35,
                    ),
                    ft.Container(
                        content=scores,
                        padding=20,
                        width=window_width * 0.23,
                        border_radius=10,
                        bgcolor=ft.colors.GREY_100,
                        height=window_height*0.70,
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.Container(
                content=tablero,
                padding=20,
                width=window_width * 0.6,
                height=window_height+100,
                border_radius=10,
                bgcolor=ft.colors.GREY_100,
                expand=True,
            )
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
    ))

    # Después de ciertos segundos se mueven las piezas a las posiciones especificadas
    # simulamos el paso de los turnos

    time.sleep(1)
    update(new_pos=new_pos)

    time.sleep(1)
    update(new_pos=new_pos2)

    time.sleep(1)
    update(new_pos=new_pos3)

    time.sleep(1)
    update(new_pos=new_pos4)

    time.sleep(1)
    update(new_pos=new_pos5)


ft.app(target=main)
# ft.app(target=main, view=ft.AppView.WEB_BROWSER)
