from flet import *
from presentation.states.active_sidebar_button_state import ActiveSideBarButtonState
from presentation.states.language_state import LanguageState
from presentation.states.accent_color_state import AccentColorState

class StartView(Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    def __init__(self):
        super().__init__()
        self.widget_scale = 1.0

        self.active_sidebar_button_state = ActiveSideBarButtonState()
        self.lang_state = LanguageState()
        self.lang_state.on_lang_updated = self.update_lang
        self.ac_state = AccentColorState()
        self.ac_state.on_colors_updated = self.update_colors

        self.padding = padding.all(16)
        self.expand = True
        self.expand_loose = True

        self.create_xilogism_span = TextSpan(
            text="CREATE MY XILOGISM\n",
            style=TextStyle(
                size=18,
                color="black",
                weight=FontWeight.W_700
            )
        )

        self.format_span = TextSpan(
            text="Pseudocode Format",
            style=TextStyle(
                size=12,
                color="black"
            )
        )

        self.new_button = FilledButton(
            on_click = lambda _: setattr(self.active_sidebar_button_state, 'active', "New Xilogism"),
            scale=transform.Scale(scale=1),
            animate_scale=animation.Animation(250, AnimationCurve.BOUNCE_OUT),
            content=Container(
                padding = padding.all(16),
                content = Row(
                    controls=[
                        Image(
                            src="/icons_light/new.png",
                            width=56,
                            height=56
                        ),
                        Text(
                            spans=[
                                self.create_xilogism_span,
                                self.format_span
                            ],
                            text_align=TextAlign.START,
                            expand=True
                        )
                    ]
                )
            ),
            style=ButtonStyle(
                bgcolor={},  # Will be set in update_colors
                shape=RoundedRectangleBorder(16),
                side=BorderSide(1, {})  # Will be set in update_colors
            ),
            on_hover=self._hover
        )

        self.open_existing_text = Text(
            value="OPEN EXISTING",
            weight=FontWeight.W_600,
            color="black",  # Will be updated in update_colors
            text_align=TextAlign.START,
            expand=True
        )

        self.open_button = FilledButton(
            scale=transform.Scale(scale=1),
            animate_scale=animation.Animation(250, AnimationCurve.BOUNCE_OUT),
            content=Container(
                padding = padding.symmetric(8 * self.widget_scale, 16),
                content = Row(
                    controls = [
                        Image(
                            src="/icons_light/open.png",
                            width=16,
                            height=16
                        ),
                        self.open_existing_text
                    ],
                )
            ),
            on_click = lambda event: setattr(self.active_sidebar_button_state, 'active', "Open Xilogism"),
            style=ButtonStyle(
                bgcolor={},  # Will be set in update_colors
                shape=RoundedRectangleBorder(16),
                side=BorderSide(1, {})  # Will be set in update_colors
            ),
            on_hover=self._hover
        )

        self.logo_icon = Image(
            src="light_mode.gif",
            width=360,
            height=360,
        )

        self.get_dirty_span = TextSpan(
            text="GET YOUR HANDS DIRTY WITH\n",
            style=TextStyle(
                size=16,
                weight=FontWeight.W_600,
                italic=True,
                color={}  # Will be set in update_colors
            )
        )

        self.code_to_circuits_text = Text(
            value="CODES TO CIRCUITS, XILOGIZED!",
            size=20,
            weight=FontWeight.W_700,
            text_align=TextAlign.CENTER,
            color={}  # Will be set in update_colors
        )

        self.content = Row(
            alignment=MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=CrossAxisAlignment.CENTER,
            expand=True,
            controls=[
                Container(
                    content = self.logo_icon,
                    expand=True
                ),
                Container(
                    expand = True,
                    content = Column(
                        expand=True,
                        alignment = MainAxisAlignment.CENTER,
                        horizontal_alignment = CrossAxisAlignment.CENTER,
                        spacing = 0,
                        controls = [
                            Text(
                                spans=[
                                    self.get_dirty_span,
                                    TextSpan(
                                        text="XILOGISM",
                                        style=TextStyle(
                                            size=72,
                                            weight=FontWeight.W_800,
                                            color={}  # Will be set in update_colors
                                        )
                                    )
                                ],
                                text_align=TextAlign.CENTER,
                                no_wrap=True
                            ),
                            self.code_to_circuits_text,
                            Container(
                                padding = padding.all(16),
                                margin = margin.symmetric(8, 0),
                                width=480,
                                height=128,
                                content = self.new_button
                            ),
                            Container(
                                padding=padding.only(left=96, right=16),
                                width=480,
                                height=48,
                                content = self.open_button,
                            )
                        ]
                    )
                )
            ]
        )
        
        # Initialize colors
        if self.ac_state.color_values:
            self.update_colors()
    
    def _hover(self, event: ControlEvent):
        button: FilledButton = event.control

        button.scale = 1.10 if event.data == "true" else 1
        button.update()
    
    def update_lang(self):
        self.create_xilogism_span.text = self.lang_state.lang_values['create_title']
        self.format_span.text = self.lang_state.lang_values["format"]
        self.open_existing_text.value = self.lang_state.lang_values["open_existing"]
        self.get_dirty_span.text = self.lang_state.lang_values["get_your_hands_dirty"]
        self.code_to_circuits_text.value = self.lang_state.lang_values["tagline"]
        self.update()
    
    def update_colors(self):
        colors = self.ac_state.color_values
        
        # Update button styles
        self.new_button.bgcolor = self.ac_state.active.value
        self.new_button.border = border.all(1, self.colors.get("divider_color", "#6d6d6d")

        self.open_button.bgcolor = self.ac_state.active.value
        self.open_button.border = border.all(1, self.colors.get("divider_color", "#6d6d6d")
        
        self.update()
