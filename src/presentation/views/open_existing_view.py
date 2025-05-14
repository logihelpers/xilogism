from flet import *
from presentation.views.widgets.existing_view import *
from presentation.states.language_state import LanguageState
from presentation.states.accent_color_state import AccentColorState
from presentation.states.dark_mode_state import *
from services.init.init_files import AppendFile

class OpenExistingView(Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    def __init__(self):
        super().__init__()

        self.lang_state = LanguageState()
        self.lang_state.on_lang_updated = self.update_lang
        self.ac_state = AccentColorState()
        self.ac_state.on_colors_updated = self.update_colors
        self.dm_state = DarkModeState()

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

        self.pick_file_dialog = FilePicker(
            on_result=self.pick_files_result
        )

        self.open_from_system = FilledButton(
            "Open from System",
            icon=Icons.FILE_OPEN_OUTLINED,
            bgcolor="#4d191f51",
            color="black",
            style=ButtonStyle(
                padding=padding.symmetric(16, 8),
                shape=RoundedRectangleBorder(8),
                side=BorderSide(1, "black")
            ),
            on_click=lambda _: self.pick_file_dialog.pick_files(
                allow_multiple=False,
                allowed_extensions=["xlg", "XLG"]
            ),
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

        self.pinned_list = Row( # Pinned row
            controls=[],
            scroll=True,
            spacing=16
        )

        self.local_list = ListView( # Local Column
            controls=[],
            expand=True,
        )

        self.content = Column(
            controls = [
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        self.greetings_text,
                        self.open_from_system
                    ]
                ),
                self.pinned_text,
                self.pinned_list,
                Container(
                    content = self.local_text,
                    padding=padding.only(top=16)
                ),
                Divider(1, color="#6b6b6b"),
                Container(
                    padding=padding.only(top=8, right=8, bottom=0, left=8),
                    content = self.local_list,
                    expand=True
                )
            ]
        )
    
    def did_mount(self):
        super().did_mount()
        self.page.overlay.append(self.pick_file_dialog)
    
    def update_lang(self):
        lang_values = self.lang_state.lang_values
        self.greetings_text.value = lang_values["greetings"]
        self.search_tf.hint_text = lang_values["search"]
        self.pinned_text.value = lang_values["pinned_projects"]
        self.local_text.value = lang_values["local_projects"]
        self.update()
    
    def update_colors(self):
        colors = self.ac_state.color_values
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        self.greetings_text.color = colors["text_color"]
        self.pinned_text.color = colors["text_color"]
        self.local_text.color = colors["text_color"]
        self.open_from_system.bgcolor = colors["button_bgcolor"].replace("4d", "0f") if "4d" in colors["button_bgcolor"] else colors["button_bgcolor"].replace("#", "#73")
        self.open_from_system.color = colors["text_color"]
        self.open_from_system.style.side = BorderSide(1, colors["text_color"])
        self.content.controls[4].color = colors["divider_color"]  # Divider

        self.update()
    
    def pick_files_result(self, e: FilePickerResultEvent):
        if e.files:
            AppendFile(e.files[0].path)