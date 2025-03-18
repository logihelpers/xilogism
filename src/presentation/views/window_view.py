from flet import *

from mediaquerycontainer import MediaQueryContainer as MediaQuery

from presentation.views.widgets.sidebar.sidebar import SideBar
from presentation.views.widgets.titlebar import TitleBar

from presentation.views.start_view import StartView
from presentation.views.open_existing_view import OpenExistingView

class WindowView(Row):
    def __init__(self):
        super().__init__()

        self.media_query = MediaQuery()
        self.sidebar = SideBar()
        self.titlebar = TitleBar()
        self.start_view = StartView()
        self.open_view = OpenExistingView()

        self.switcher = AnimatedSwitcher(
            content = self.start_view,
            transition= AnimatedSwitcherTransition.FADE,
            duration=250,
            reverse_duration=250,
            switch_in_curve= AnimationCurve.LINEAR,
            switch_out_curve= AnimationCurve.LINEAR,
            expand=True
        )

        self.controls = [
            self.media_query,
            self.sidebar,
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