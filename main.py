from components import *
import tensorflow as tf
import flet as ft


def update(new_pos):
    if new_pos is not None:
        new_pos_filtered = tablero.filter_out_eliminated_players(new_pos)
        tablero.update_pos(new_pos_filtered)
        scores.update_scores(new_pos_filtered)


def update_game(e):
    new_pos = menu.connection.cam.get_pieces()
    update(new_pos)


scores = Scores()
tablero = Tablero(scores=scores)
menu = Menu(fn_update=update_game)


def hello_world(e):
    print("Hello World")


def main(page: ft.Page):

    page.title = "AI Chess"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.START
    page.window_maximized = True
    window_width = page.window_width
    window_height = page.window_height
    page.window_full_screen = True
    page.scroll = True

    def zoom_in(e):
        if app.scale >= 1:
            return
        app.scale += 0.1
        page.update()

    def zoom_out(e):
        app.scale -= 0.1
        page.update()

    def exit_game(e):
        page.window_close()

    def full_screen(e):
        page.window_full_screen = not page.window_full_screen
        page.update()

    app = ft.Row(
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
        scale=1
    )

    app_exit_btn = ft.Container(
        ft.IconButton(icon="close", on_click=exit_game, width=35,
                      height=35, icon_color=ft.colors.WHITE),
        bgcolor=ft.colors.RED_500,
        border_radius=10,
    )

    app_minimize_btn = ft.Container(
        ft.IconButton(icon="FULLSCREEN_EXIT", on_click=full_screen,
                      width=35, height=35, icon_color=ft.colors.WHITE),
        bgcolor=ft.colors.BLUE_500,
        border_radius=10,
    )

    app_bar = ft.Container(
        ft.Row(
            [
                ft.Row(
                    [ft.Container(
                        ft.IconButton(icon="ADD", on_click=zoom_in, width=35,
                                      height=35, icon_color=ft.colors.WHITE),
                        bgcolor=ft.colors.BLUE_500,
                        border_radius=10,
                    ),
                        ft.Container(
                            ft.IconButton(icon="remove", on_click=zoom_out,
                                          width=35, height=35, icon_color=ft.colors.WHITE),
                            bgcolor=ft.colors.BLUE_500,
                            border_radius=10,
                    ),
                        ft.Container(
                            ft.IconButton(icon="ROTATE_90_DEGREES_CW_OUTLINED", on_click=tablero.rotate_board,
                                          width=35, height=35, icon_color=ft.colors.WHITE),
                            bgcolor=ft.colors.BLUE_500,
                            border_radius=10,
                    )
                    ], spacing=1),
                ft.Row([app_minimize_btn,
                        app_exit_btn],
                       alignment=ft.MainAxisAlignment.END,
                       spacing=1)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=ft.colors.GREY_100,
        border_radius=10,
    )

    page.add(app_bar, app)


ft.app(target=main)
