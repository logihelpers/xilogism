import flet as ft
import splash

from presentation.controllers import InitControllers

async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed = "#4169e1"
    )
    page.fonts = {
        "Product Sans" : "/fonts/Product Sans Regular.ttf",
        "Inter" : "/fonts/Inter.ttf"
    }
    page.theme = ft.Theme(color_scheme_seed = "#4169e1", font_family="Inter")
    page.window.title_bar_hidden = True
    page.window.center()
    page.padding = ft.padding.all(0)
    page.window.min_height = 600
    page.window.min_width = 980
    page.window.width = 980
    page.window.height = 600
    page.spacing = 0
    page.bgcolor = "#ededed"

    # start_view = StartView()
    
    # open_existing_view = OpenExistingView()

    # switcher = ft.AnimatedSwitcher(
    #     content = start_view,
    #     transition=ft.AnimatedSwitcherTransition.FADE,
    #     duration=250,
    #     reverse_duration=250,
    #     switch_in_curve=ft.AnimationCurve.LINEAR,
    #     switch_out_curve=ft.AnimationCurve.LINEAR,
    #     expand=True
    # )

    # def switch_child():
    #     switcher.content = open_existing_view if switcher.content == start_view else start_view
    #     switcher.update()

    # sidebar.new = switch_child

    # def size_change(event: MediaQueryContainerChangeEvent):
    #     scale: float = 1 + (((event.window_width / 967.2) - 1) / 2)

    #     sidebar.scale_all(scale)
    #     titlebar.scale_all(scale)

    #     switcher.content.scale_all(scale)

    InitControllers(target=page)

# ft.app(splash.app)
ft.app(main)