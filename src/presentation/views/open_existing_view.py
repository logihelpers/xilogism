from flet import *
from presentation.views.widgets.existing_view import *
from presentation.states.language_state import LanguageState

class OpenExistingView(Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    def __init__(self):
        super().__init__()

        self.lang_state = LanguageState()
        self.lang_state.on_lang_updated = self.update_lang

        self.widget_scale = 1.0
        self.padding = padding.all(16 * self.widget_scale)
        self.expand = True

        self.greetings_text = Text(
            "Greetings, my friend!",
            color="black",
            weight=FontWeight.W_700,
            italic=True,
            size=28
        )

        self.search_tf = TextField(
            content_padding=padding.symmetric(4, 24),
            width=256,
            border_radius=32,
            bgcolor="#26191f51",
            border=border.all(1, "black"),
            icon=Image(
                src="/icons_light/search.png",
                width=24,
                height=24
            ),
            hint_text="Search",
            hint_style=TextStyle(
                color="black",
                weight=FontWeight.W_500,
                size=14,
            )
        )

        self.pinned_text = Text(
            "Pinned Projects",
            weight=FontWeight.W_500,
            size=14
        )

        self.local_text = Text(
            "Local Projects",
            weight=FontWeight.W_500,
            size=14
        )

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
                Divider(1, color="#6b6b6b"),
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
        self.greetings_text.value = self.lang_state.lang_values["greetings"]
        self.search_tf.hint_text = self.lang_state.lang_values["search"]
        self.pinned_text.value = self.lang_state.lang_values["pinned_projects"]
        self.local_text.value = self.lang_state.lang_values["local_projects"]
        self.update()