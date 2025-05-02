from flet import *
from presentation.views.widgets.existing_view import *
from presentation.states.language_state import LanguageState
from presentation.states.accent_color_state import AccentColorState

class OpenExistingView(Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    def __init__(self):
        super().__init__()

        self.lang_state = LanguageState()
        self.lang_state.on_lang_updated = self.update_lang
        self.ac_state = AccentColorState()
        self.ac_state.on_colors_updated = self.update_colors

        # Get current theme colors
        self.colors = self.ac_state.color_values

        self.widget_scale = 1.0
        self.padding = padding.all(16 * self.widget_scale)
        self.expand = True

        self.greetings_text = Text(
            "Greetings, my friend!",
            color=self.colors.get("text_color", "#000000"),
            weight=FontWeight.W_700,
            italic=True,
            size=28
        )

        self.search_tf = TextField(
            content_padding=padding.symmetric(4, 24),
            width=256,
            border_radius=32,
            bgcolor=self.ac_state.active.value,
            border=border.all(1, self.colors.get("divider_color", "#6d6d6d")),
            icon=Image(
                src="/icons_light/search.png",
                width=24,
                height=24
            ),
            hint_text="Search",
            hint_style=TextStyle(
                color=self.colors.get("text_color", "#000000"),
                weight=FontWeight.W_500,
                size=14,
            )
        )

        self.pinned_text = Text(
            "Pinned Projects",
            color=self.colors.get("text_color", "#000000"),
            weight=FontWeight.W_500,
            size=14
        )

        self.local_text = Text(
            "Local Projects",
            color=self.colors.get("text_color", "#000000"),
            weight=FontWeight.W_500,
            size=14
        )

        self.divider = Divider(1, color=self.colors.get("divider_color", "#6d6d6d"))

        self.content = Column(
            controls = [
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        self.greetings_text,
                        self.search_tf
                    ]
                ),
                self.pinned_text,
                Row( # Pinned row
                    controls=[
                        PinnedButton(),
                        PinnedButton(),
                        PinnedButton(),
                        PinnedButton(),
                        PinnedButton(),
                        PinnedButton()
                    ],
                    scroll=True,
                    spacing=16
                ),
                Container(
                    content = self.local_text,
                    padding=padding.only(top=16)
                ),
                self.divider,
                Container(
                    padding=padding.only(top=8, right=8, bottom=0, left=8),
                    content = Column( # Local Column
                        controls=[
                            LocalButton(),
                            LocalButton(),
                            LocalButton(),
                            LocalButton(),
                            LocalButton(),
                            LocalButton(),
                            LocalButton()
                        ],
                        expand=True,
                        scroll=True
                    ),
                    expand=True
                )
            ]
        )
    
    def update_lang(self):
        lang_values = self.lang_state.lang_values
        self.greetings_text.value = lang_values["greetings"]
        self.search_tf.hint_text = lang_values["search"]
        self.pinned_text.value = lang_values["pinned_projects"]
        self.local_text.value = lang_values["local_projects"]
        self.update()
    
    def update_colors(self):
        self.colors = self.ac_state.color_values
        
        # Update text colors
        self.greetings_text.color = self.colors.get("text_color", "#000000")
        self.pinned_text.color = self.colors.get("text_color", "#000000")
        self.local_text.color = self.colors.get("text_color", "#000000")
        
        # Update search text field
        self.search_tf.bgcolor = self.ac_state.active.value
        self.search_tf.border = border.all(1, self.colors.get("divider_color", "#6d6d6d"))
        self.search_tf.hint_style = TextStyle(
            color=self.colors.get("text_color", "#000000"),
            weight=FontWeight.W_500,
            size=14,
        )
        
        # Update divider
        self.divider.color = self.colors.get("divider_color", "#6d6d6d")
        
        # Update the view
        self.update()
