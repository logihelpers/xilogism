import flet as ft
import asyncio

async def app(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {"Product Sans" : "/Product Sans Regular.ttf"}
    page.theme = ft.Theme(color_scheme_seed = "#4169e1", font_family="Product Sans")
    page.window.title_bar_hidden = True
    page.window.width = 600
    page.window.height = 300
    page.window.center()

    image = ft.Image(src="/icon.png", width=150, fit=ft.ImageFit.SCALE_DOWN)

    pr = ft.ProgressRing(width=16, height=16, stroke_width = 2)

    page.add(
        ft.Row(
            [
                image,
                ft.Text("Logihelp", size=96, color="#1d2357", weight=ft.FontWeight.W_500)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        ft.Row(
            [
                pr,
                ft.Text("Please wait while we set a few things up for you.", size=16, color="#1d2357"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
    )

    await asyncio.sleep(2)
    page.window.close()