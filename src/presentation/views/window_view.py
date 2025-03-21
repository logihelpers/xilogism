from flet import *

from mediaquerycontainer import MediaQueryContainer as MediaQuery

from presentation.views.widgets.sidebar.sidebar import SideBar
from presentation.views.widgets.titlebar import TitleBar

from presentation.views.start_view import StartView
from presentation.views.editor_view import EditorView
from presentation.views.open_existing_view import OpenExistingView

from slidablepanel import SlidablePanel
from xiloswitcher import XiloSwitcher

class WindowView(Row):
    def __init__(self):
        super().__init__()

        self.media_query = MediaQuery()
        self.sidebar = SideBar()
        self.titlebar = TitleBar()

        self.start_view = StartView()
        self.editor_view = EditorView()
        self.open_view = OpenExistingView()

        self.slidable_panel = SlidablePanel(
            sidebar=self.sidebar
        )

        self.switcher = XiloSwitcher(
            expand=True,
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