import flet as ft
from components import *

text = ft.Text("Hello World")

def main(page: ft.Page):

  rail = ft.NavigationRail(
      selected_index=0,
      label_type=ft.NavigationRailLabelType.ALL,
      min_width=100,
      min_extended_width=400,
      destinations=[
          ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.WIFI), label="Wifi"),
          ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.USB), label="Usb")
      ],
      on_change= lambda e : print("Selected destination:", e.control.selected_index), 
  )

  # Structure the layout with Row and Column
  page.add(
    ft.Row(
    [
    rail,
    ft.VerticalDivider(width=1),
    ft.Column([ text], alignment=ft.MainAxisAlignment.START, expand=True),
    ],
    expand=True,
  ))

ft.app(target=main)