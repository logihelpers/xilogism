import flet as ft
import asyncio

async def app(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {"Inter" : "/fonts/Inter.ttf"}
    page.theme = ft.Theme(color_scheme_seed = "#4169e1", font_family="Inter")
    page.window.title_bar_hidden = True
    page.window.width = 640
    page.window.height = 300
    page.window.center()

    image = ft.Image(src="/icon.png", width=200, height = 200, fit=ft.ImageFit.SCALE_DOWN)

    pr = ft.ProgressRing(width=16, height=16, stroke_width = 2)

    page.add(
        ft.Row(
            [
                image,
                ft.Column(
                    controls = [
                        ft.Text("Logihelp", size=96, color="#191f51", weight=ft.FontWeight.W_500),
                        ft.Text("Code to Circuits? Xilogized!", size=16, color="black", weight=ft.FontWeight.W_500)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        ft.Row(
            [
                pr,
                ft.Text("Please wait while we set a few things up for you.", size=16, color="black"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
    )

    await asyncio.sleep(5)
    page.window.close()