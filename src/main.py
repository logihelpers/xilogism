import flet as ft
import splash
import titlebar as tb
import sidebar as sb

from views.start_view import StartView
from views.editor_view import EditorView

from logic_circuit.gates.not_gate import NOTGate
from logic_circuit.gates.and_gate import ANDGate
from logic_circuit.gates.or_gate import ORGate
from logic_circuit.gates.xor_gate import XORGate
from logic_circuit.input_node import InputNode
from logic_circuit.output_node import OutputNode
from logic_circuit.wire import Wire
from logic_circuit.canvas import LogicCanvas

async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed = "#4169e1"
    )
    page.fonts = {
        "Product Sans" : "/Product Sans Regular.ttf",
        "Inter" : "/Inter.ttf"
    }
    page.theme = ft.Theme(color_scheme_seed = "#4169e1", font_family="Inter")
    page.window.title_bar_hidden = True
    page.window.center()
    page.padding = ft.padding.all(0)
    page.window.width = 1280
    page.window.height = 768
    page.spacing = 0
    page.bgcolor = "#ededed"

    page.appbar = tb.Titlebar()

    start_view = StartView()
    editor_view = EditorView()

    switcher = ft.AnimatedSwitcher(
        start_view,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=300,
        reverse_duration=100,
        switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
        switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
        expand=True
    )
    
    page.add(switcher)

    def show_editor_view(event):
        page.appbar.home_button.visible = True
        page.appbar.home_button.update()

        switcher.content = editor_view
        switcher.update()

    start_view.sidebar.new_button.on_click = show_editor_view

    def show_start_view(event):
        page.appbar.home_button.visible = False
        page.appbar.home_button.update()

        switcher.content = start_view
        switcher.update()

    page.appbar.home_button.on_click = show_start_view

    first_login = await page.client_storage.get_async("first-login")
    if first_login is None:
        await page.client_storage.set_async("first-login", False)

# ft.app(splash.app)
ft.app(main)