from flet import *

from presentation.views.widgets.sidebar.sidebar import SideBar
from presentation.views.widgets.titlebar import TitleBar

from presentation.views.start_view import StartView
from presentation.views.editor_view import EditorView
from presentation.views.open_existing_view import OpenExistingView

from presentation.views.dialogs.settings_dialog import SettingsDialog

from xilowidgets import MediaQuery, Revealer, Switcher

class WindowView(Row):
    def __init__(self):
        super().__init__()
    
    def build(self):
        super().build()

        self.media_query = MediaQuery()
        self.sidebar = SideBar()
        self.titlebar = TitleBar()

        self.start_view = StartView()
        self.editor_view = EditorView()
        self.open_view = OpenExistingView()

        self.settings_dialog = SettingsDialog()

        self.slidable_panel = Revealer(
            content=self.sidebar,
            content_hidden=False,
        )

        self.switcher = Switcher(
            expand=True,
            orientation=Switcher.Orientation.VERTICAL,
            controls=[
                self.start_view,
                self.editor_view,
                self.open_view,
                Container(Text("1"), bgcolor=Colors.random()),
                Container(Text("2"), bgcolor=Colors.random()),
                Container(Text("3"), bgcolor=Colors.random()),
                Container(Text("4"), bgcolor=Colors.random()),
                Container(Text("5"), bgcolor=Colors.random()),
                Container(Text("6"), bgcolor=Colors.random()),
                Container(Text("7"), bgcolor=Colors.random()),
                Container(Text("8"), bgcolor=Colors.random()),
                Container(Text("9"), bgcolor=Colors.random()),
            ]
        )

        self.controls = [
            self.media_query,
            self.slidable_panel,
            Container(
                expand = True,
                padding = padding.symmetric(8, 0),
                content=Column(
                    expand = True,
                    controls=[
                        self.titlebar,
                        self.switcher
                    ]
                )
            )
        ]

        self.spacing=0
        self.expand=True
        self.vertical_alignment = CrossAxisAlignment.STRETCH