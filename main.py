from components import *
import flet as ft
import time

def main(page: ft.Page):
    page.title = "AI Chess"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.START
    page.window_maximized = True
    page.scroll = True
    menu = Menu()
    tablero = Tablero()
    scores = Scores()
    # Ejemplo de las posiciones obtenidas de la IA (sirve para calcular los scores de las piezas y
    # mostrarlas las piezas en la interfaz gráfica)
    new_pos = [
        {"id": "D14", "img": "AZ"},
        {"id": "E14", "img": "PN"},
        {"id": "F14", "img": "TR"},
        {"id": "G14", "img": "QA"},
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
                        width=300,
                        border_radius=10,
                        height=250
                    ),
                    ft.Container(
                        content=scores,
                        padding=20,
                        width=300,
                        border_radius=10,
                        bgcolor=ft.colors.GREY_100,
                        height=510,
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.Container(
                content=tablero,
                padding=20,
                width=900,
                height=775,
                border_radius=10,
                bgcolor=ft.colors.GREY_100,
                expand=True
            )
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
    ))

    # Después de 3 segundos se mueven las piezas a las posiciones especificadas
    time.sleep(1)
    tablero.update_pos(new_pos)
    scores.update_scores(new_pos)

ft.app(target=main)
#ft.app(target=main, view=ft.AppView.WEB_BROWSER)


