from flet import *
from utils.singleton import Singleton
from xilowidgets import XDialog

from presentation.states.new_save_state import NewSaveState
from presentation.states.dialogs_state import Dialogs, DialogState
from presentation.states.language_state import LanguageState
from presentation.states.accent_color_state import AccentColorState

class CreateNewDialog(XDialog, metaclass = Singleton):
    def __init__(self):
        super().__init__()

        self.dia_state = DialogState()
        self.ns_state = NewSaveState()
        self.lang_state = LanguageState()
        self.ac_state = AccentColorState()

        self.elevation = 0
        self.content_padding = 8
        self.title_padding = 0
        self.clip_behavior = ClipBehavior.HARD_EDGE
        self.bgcolor = "#ededed"
        self.actions_padding = padding.all(16)
        self.action_button_padding = 0
        self.actions_overflow_button_spacing = 0
        self.open_duration = 300
        self.modal = True

        self.save_button = FilledButton(
            "Save", 
            width=128,
            bgcolor="#191f51",
            color="white",
            style=ButtonStyle(
                shape=RoundedRectangleBorder(8),
                padding=8
            ),
            disabled = True,
            on_click=self.trigger_save
        )

        self.actions=[
            self.save_button,
            FilledButton(
                "Close", 
                width=128,
                style=ButtonStyle(
                    color="black",
                    shape=RoundedRectangleBorder(8),
                    padding=8,
                    bgcolor="#36191f51"
                ),
                on_click=self.trigger_save
            )
        ]
        self.actions_alignment=MainAxisAlignment.SPACE_BETWEEN

        self.proj_name_tf = TextField(hint_text="e.g. Xilogism 1", expand = True, on_change=self.validate_fields)
        self.file_path_tf = TextField(hint_text="e.g. xilogism_1", suffix_text=".xlg", expand = True, on_change=self.validate_fields)

        self.content = Container(
            padding = 8,
            height=180,
            width=400,
            expand=True,
            content = Column(
                expand=True,
                horizontal_alignment=CrossAxisAlignment.STRETCH,
                spacing=0,
                controls=[
                    Container(
                        content = Text("Do you want to save your new Xilogism?", size=16, weight=FontWeight.BOLD),
                        padding=padding.symmetric(16, 0)
                    ),
                    Container(
                        expand = True,
                        padding = padding.symmetric(0, 16),
                        content = Column(
                            expand = True,
                            controls = [
                                Row(
                                    height = 36,
                                    controls=[
                                        Text("Project Name: ", weight=FontWeight.W_500, width=100),
                                        self.proj_name_tf
                                    ],
                                    expand = True
                                ),
                                Row(
                                    height = 36,
                                    controls=[
                                        Text("Filename: ", weight=FontWeight.W_500, width=100),
                                        self.file_path_tf
                                    ],
                                    expand = True
                                )
                            ]
                        )
                    )
                ]
            )
        )
    
    def trigger_save(self, event: ControlEvent):
        if event.control.text == "Save":
            self.ns_state.filename = self.file_path_tf.value
            self.ns_state.project_name = self.proj_name_tf.value
            self.ns_state.state = True
        else:
            self.ns_state.filename = ""
            self.ns_state.project_name = ""
            self.ns_state.state = False
        
        self.dia_state.state = Dialogs.CLOSE
    
    def validate_fields(self, event: ControlEvent):
        if self.proj_name_tf.value != "" and self.file_path_tf.value != "":
            self.save_button.disabled = False
        else:
            self.save_button.disabled = True
        
        self.save_button.update()
    
    def did_mount(self):
        super().did_mount()
        self.lang_state.on_lang_updated = self.update_lang
        self.update_lang()
        self.ac_state.on_colors_updated = self.update_colors
        self.update_colors()
    
    def update_colors(self):
        colors = self.ac_state.color_values
        self.bgcolor = colors["bg_color"]
        self.content.content.controls[0].content.color = colors["text_color"]  # Save prompt
        self.content.content.controls[1].content.controls[0].controls[0].color = colors["text_color"]  # Project Name
        self.content.content.controls[1].content.controls[1].controls[0].color = colors["text_color"]  # Filename
        self.proj_name_tf.bgcolor = colors["field_bgcolor"]
        self.proj_name_tf.border_color = colors["field_border_color"]
        self.file_path_tf.bgcolor = colors["field_bgcolor"]
        self.file_path_tf.border_color = colors["field_border_color"]
        self.save_button.style = ButtonStyle(
            bgcolor=colors["save_button_bgcolor"],
            side=BorderSide(1, colors["button_border_color"]),
            shape=RoundedRectangleBorder(8),
            padding=8
        )
        self.save_button.color = colors["text_color"]
        self.actions[1].style = ButtonStyle(
            bgcolor=colors["button_bgcolor"],
            side=BorderSide(1, colors["button_border_color"]),
            shape=RoundedRectangleBorder(8),
            padding=8
        )
        self.actions[1].color = colors["text_color"]
        self.update()
    
    def update_lang(self):
        lang_values = self.lang_state.lang_values
        self.content.content.controls[0].content.value = lang_values["save_prompt"]
        self.content.content.controls[1].content.controls[0].controls[0].value = lang_values["project_name_label"]
        self.content.content.controls[1].content.controls[1].controls[0].value = lang_values["filename_label"]
        self.save_button.text = lang_values["save_button"]
        self.actions[1].text = lang_values["close_button"]
        self.proj_name_tf.hint_text = lang_values["project_name_hint"]
        self.file_path_tf.hint_text = lang_values["filename_hint"]
        self.file_path_tf.suffix_text = lang_values["file_extension"]
        self.update()