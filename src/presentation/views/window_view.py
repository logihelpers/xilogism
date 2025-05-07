from flet import *

from presentation.views.widgets.sidebar.sidebar import SideBar
from presentation.views.widgets.titlebar import TitleBar

from presentation.views.start_view import StartView
from presentation.views.editor_view import EditorView
from presentation.views.open_existing_view import OpenExistingView

from presentation.views.dialogs.settings_dialog import SettingsDialog

from presentation.states.media_query_state import MediaQueryState
from presentation.states.accent_color_state import AccentColorState
from presentation.states.animation_disable_state import AnimationDisableState

from xilowidgets import MediaQuery, Revealer, Switcher

class WindowView(Row):
    def __init__(self):
        super().__init__()
    
    def build(self):
        super().build()

        self.mq_state = MediaQueryState()
        self.ac_state = AccentColorState()
        self.ac_state.on_colors_updated = self.update_colors
        self.ad_state = AnimationDisableState()
        self.ad_state.on_change = self.update_animations

        self.media_query = MediaQuery(on_size_change=lambda e: setattr(self.mq_state, 'size', (e.window_width, e.window_height)))
        self.sidebar = SideBar(self.page)
        if hasattr(self, "page"):
            self.page.sidebar = self.sidebar
        self.titlebar = TitleBar()

        self.start_view = StartView()
        self.editor_view = EditorView("New")
        self.open_view = OpenExistingView()

        self.settings_dialog = SettingsDialog()

        self.slidable_panel = Revealer(
            content=self.sidebar,
            content_hidden=False,
            animation_curve=AnimationCurve.EASE_IN_OUT_CUBIC,
            animation_duration=500
        )

        self.switcher = Switcher(
            expand=True,
            orientation=Switcher.Orientation.VERTICAL,
            animation_curve=AnimationCurve.EASE_IN_OUT_CIRC,
            animation_duration=500,
            controls=[
                self.start_view,
                self.editor_view,
                self.open_view,
            ]
        )

        self.main_container = Container(
            expand = True,
            padding = padding.only(top=8),
            content=Column(
                expand = True,
                controls=[
                    self.titlebar,
                    self.switcher
                ]
            ),
        )

        self.controls = [
            self.media_query,
            self.slidable_panel,
            self.main_container
        ]

        self.spacing=0
        self.expand=True
        self.vertical_alignment = CrossAxisAlignment.STRETCH
    
    def update_colors(self):
        colors = self.ac_state.color_values
        self.page.bgcolor = colors["bg_color"]
        self.page.update()
    
    def update_animations(self):
        animate = self.ad_state.state
        self.slidable_panel.animation_duration = 500 if animate else 0
        self.switcher.animation_duration = 500 if animate else 25
        self.update()