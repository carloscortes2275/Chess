from components import * 
import flet as ft

def main(page: ft.Page):
    page.title = "Tablero "
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.START
    page.window_max_width = 1200
    page.window_max_height = 800

    m = Menu()
    page.add(ft.Container(
          content=m,
          bgcolor=ft.colors.GREY_100,
          padding=20,
          width=300,
          border_radius=10,
          height=300
    ))


ft.app(target=main)