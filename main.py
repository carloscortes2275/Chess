from components import *
import tensorflow as tf
import flet as ft


def main(page: ft.Page):

    page.title = "AI Chess"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.START
    page.window_maximized = True
    window_width = page.window_width
    window_height = page.window_height
    page.window_full_screen = False
    page.scroll = True

    def update(new_pos):
        if new_pos is not None:
            new_pos_filtered = tablero.filter_out_eliminated_players(new_pos)
            tablero.update_pos(new_pos_filtered)
            scores.update_scores(new_pos_filtered)

    def update_game(e):
        new_pos = menu.connection.cam.get_pieces()
        update(new_pos)

    def open_dlg(page, player: str):
        page.dialog = winner
        winner.title = ft.Text(f"Winner is : ", color="green", size=35,
                               text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)
        winner.content = ft.Text(f"{player}\n\n 🎉Congratulations, you won the game! 🎉",
                                 size=20, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)
        # winner.content=ft.Text(f"{player}\n\n Congratulations, you won the game! ",size=20,text_align=ft.TextAlign.CENTER)
        winner.open = True
        page.update()

    scores = Scores()
    menu = Menu(fn_update=update_game)
    tablero = Tablero(scores=scores, fn_show_winner=open_dlg,
                      page=page, menu=menu)

    def close_dlg(e):
        winner.open = False
        page.update()

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
        tooltip="Exit",
    )

    app_minimize_btn = ft.Container(
        ft.IconButton(icon="FULLSCREEN_EXIT", on_click=full_screen,
                      width=35, height=35, icon_color=ft.colors.WHITE),
        bgcolor=ft.colors.BLUE_500,
        border_radius=10,
        tooltip="switch screen-mode",
    )

    winner = ft.AlertDialog(
        modal=True,
        actions=[
            ft.TextButton("Exit", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
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
                        tooltip="Zoom in",
                    ),
                        ft.Container(
                            ft.IconButton(icon="remove", on_click=zoom_out,
                                          width=35, height=35, icon_color=ft.colors.WHITE),
                            bgcolor=ft.colors.BLUE_500,
                            border_radius=10,
                            tooltip="Zoom out",
                    ),
                        ft.Container(
                            ft.IconButton(icon="ROTATE_90_DEGREES_CW_OUTLINED", on_click=tablero.rotate_board,
                                          width=35, height=35, icon_color=ft.colors.WHITE),
                            bgcolor=ft.colors.BLUE_500,
                            border_radius=10,
                            tooltip="Rotate board",
                    ),
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
