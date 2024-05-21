from components import *
import flet as ft
import time

def main(page: ft.Page):
    page.title = "AI Chess"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.START
    page.window_maximized = True
    page.theme_mode = ft.ThemeMode.LIGHT

    menu = Menu()
    tablero = Tablero()

    # Ejemplo de las posiciones de las piezas en la parte superior del tablero
    new_pos = [
        {"id": "D14", "img": "AZ", "top": 0, "left": 0},
        {"id": "E14", "img": "PN", "top": 0, "left": 50},
        {"id": "F14", "img": "TR", "top": 0, "left": 100},
        {"id": "G14", "img": "QA", "top": 0, "left": 150},
        {"id": "H14", "img": "QZ", "top": 0, "left": 200}
    ]

    # Contenedor para mostrar las puntuaciones
    score_text = ft.Text("Calculando puntuaciones...", color=ft.colors.BLACK)

    def update_scores():
        scores = tablero.calculate_scores()
        score_text.value = (f"Puntuación Azul: {scores['Z']}\n"
                            f"Puntuación Amarillo: {scores['A']}\n"
                            f"Puntuación Negro: {scores['N']}\n"
                            f"Puntuación Rojo: {scores['R']}")
        page.update()

    # Inicialmente, calcula y muestra las puntuaciones
    update_scores()

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
                        content=score_text,
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
    time.sleep(3)
    tablero.update_pos(new_pos)
    update_scores()

ft.app(target=main)
