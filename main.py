from components import *
import flet as ft
import time


def main(page: ft.Page):
    page.title = "AI Chess"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.START
    # page.window_full_screen = True
    page.window_maximized = True
    menu = Menu()
    tablero = Tablero()

    # ejemplo de los valores que tenemos que obtener de la IA (posicion de la pieza e identificador de la pieza)
    # AN (AlfilNegro)
    new_pos = [{"id": "D14", "img": "AN"}, {'id': 'E14', 'img': 'AN'}]

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
                        content=ft.Text(
                            "Aqui va el componente de puntuacion", color=ft.colors.BLACK),
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
    )
    )
    
    # despues de 5 segundos se mueve la pieza a la derecha usando tablero.update_pos()
    # para probar actualizar la posicion de la pieza
    time.sleep(3)
    tablero.update_pos(new_pos)
    page.update()


ft.app(target=main)
