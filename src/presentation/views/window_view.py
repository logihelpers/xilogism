from flet import *

from mediaquerycontainer import MediaQueryContainer as MediaQuery, MediaQueryContainerChangeEvent

from presentation.views.widgets.sidebar import SideBar
from presentation.views.widgets.titlebar import TitleBar

from presentation.views.start_view import StartView

class WindowView(Row):
    def __init__(self):
        super().__init__()

        self.media_query = MediaQuery()
        self.sidebar = SideBar()
        self.titlebar = TitleBar()
        self.start_view = StartView()

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
                        AnimatedSwitcher(
                            content = self.start_view,
                            transition= AnimatedSwitcherTransition.FADE,
                            duration=250,
                            reverse_duration=250,
                            switch_in_curve= AnimationCurve.LINEAR,
                            switch_out_curve= AnimationCurve.LINEAR,
                            expand=True
                        )
                    ]
                )
            )
        ]

        self.spacing=0
        self.expand=True
        self.vertical_alignment = CrossAxisAlignment.STRETCH