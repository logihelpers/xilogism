import flet as ft
import flet.canvas as cv
import numpy as np

def get_x_for_y(y):
    x = 50 * y - y ** 2
    return x

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    start_x = 350
    start_y = 75

    not_gate = cv.Canvas(
        shapes = [
            cv.Path(
                [
                    cv.Path.MoveTo(start_x, start_y),
                    cv.Path.QuadraticTo(start_x + 25, start_y, start_x + 50, start_y + 25, 1.5),
                    cv.Path.MoveTo(start_x + 50, start_y + 25),
                    cv.Path.QuadraticTo(start_x + 25, start_y + 50, start_x, start_y + 50, 1.5),
                    cv.Path.MoveTo(start_x, start_y + 50),
                    cv.Path.QuadraticTo(start_x + 25, start_y + 25, start_x, start_y)
                ],
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.STROKE,
                )
            ),
        ]
    )

    print(get_x_for_y(25))

    page.add(not_gate)

ft.app(main)