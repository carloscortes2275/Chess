from components import * 
import flet as ft

def main(page: ft.Page):
    page.title = "Tablero "
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.START
    page.window_max_width = 1200
    page.window_max_height = 800

    conn_c = Conn_camera("IP adress")

    m = Menu()
    page.add(
        ft.Row(
        [
        m,
        ft.VerticalDivider(width=1),
        ft.Column([ conn_c]),
        ],
        expand=True,
  ))


ft.app(target=main)