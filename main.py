from components import * 
import flet as ft

def main(page: ft.Page):
    page.title = "Tablero "
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_max_width = 1200
    page.window_max_height = 800
    #page.theme = ft.theme.Theme(color_scheme_seed="green")
    #page.bgcolor = "#202020"
  
    conn_came = Conn_camera("IP direction of the phone:")
    page.add(conn_came)

ft.app(target=main)