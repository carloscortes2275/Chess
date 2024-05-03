from camera import Camera
import flet as ft

def main(page: ft.Page):
    page.title = "Tablero "
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_max_width = 400
    page.window_max_height = 400
    page.window_width = 400
    page.window_height = 400
    txt_ip = ft.TextField(value="", width=365)

    def mostrar_video_click(e):
        cam = Camera(txt_ip.value)
        cam.mostrar_video()

    def close_click(e):
        page.window_close()


    page.add(
        ft.Text("Ingrese direccion IP del telefono: "),
        ft.Row(
            [ 
                txt_ip,
            ],
            alignment=ft.MainAxisAlignment.START,

        ),
        ft.Row(
            [
                ft.TextButton("Mostrar video", on_click=mostrar_video_click),
                ft.TextButton("Cerrar", on_click=close_click),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
    )

ft.app(target=main)