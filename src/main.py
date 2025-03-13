import flet as ft
import splash

import asyncio

from mediaquerycontainer import MediaQueryContainer, MediaQueryContainerChangeEvent

from ui.widgets.sidebar import SideBar
from ui.widgets.titlebar import TitleBar
from ui.views.start_view import StartView
from ui.views.open_existing_view import OpenExistingView

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

    sidebar = SideBar()
    sidebar.animate=ft.animation.Animation(250, ft.AnimationCurve.LINEAR)

    async def hide_sidebar(event):
        if not sidebar.visible:
            sidebar.visible = True
            sidebar.update()
            await asyncio.sleep(0.05)

        sidebar.offset = ft.transform.Offset(-1, 0) if sidebar.offset.x == 0 else ft.transform.Offset(0, 0)
        sidebar.update()

    start_view = StartView()
    
    def hide(event):
        if sidebar.offset == ft.transform.Offset(-1, 0):
            sidebar.visible = False if sidebar.visible else True
            sidebar.update()
    
    titlebar = TitleBar()
    titlebar.sidebar_hide_button.on_click = hide_sidebar

    sidebar.on_animation_end = hide
    
    open_existing_view = OpenExistingView()

    switcher = ft.AnimatedSwitcher(
        content = start_view,
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=250,
        reverse_duration=250,
        switch_in_curve=ft.AnimationCurve.LINEAR,
        switch_out_curve=ft.AnimationCurve.LINEAR,
        expand=True
    )

    def switch_child():
        switcher.content = open_existing_view if switcher.content == start_view else start_view
        switcher.update()

    sidebar.new = switch_child

    def size_change(event: MediaQueryContainerChangeEvent):
        scale: float = 1 + (((event.window_width / 967.2) - 1) / 2)

        sidebar.scale_all(scale)
        titlebar.scale_all(scale)

        switcher.content.scale_all(scale)

    main_child = ft.Row(
        controls=[
            MediaQueryContainer(on_media_query_change=size_change),
            sidebar,
            ft.Container(
                expand = True,
                padding = ft.padding.symmetric(8, 0),
                content=ft.Column(
                    expand = True,
                    controls=[
                        titlebar,
                        switcher
                    ]
                )
            )
        ],
        spacing=0,
        expand=True, 
        vertical_alignment=ft.CrossAxisAlignment.STRETCH
    )

    page.add(main_child)

# ft.app(splash.app)
ft.app(main)