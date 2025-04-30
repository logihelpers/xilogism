from flet import *
from services.singleton import Singleton
from xilowidgets import XDialog

from presentation.states.new_save_state import NewSaveState
from presentation.states.dialogs_state import Dialogs, DialogState

class CreateNewDialog(XDialog, metaclass = Singleton):
    def __init__(self):
        super().__init__()

        self.dia_state = DialogState()
        self.ns_state = NewSaveState()

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