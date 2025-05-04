from flet import *
from presentation.states.dialogs_state import DialogState, Dialogs
from presentation.states.render_state import RenderState
from presentation.states.export_state import ExportState, FileFormat
from presentation.states.animation_disable_state import AnimationDisableState

from xilowidgets import Revealer, XDialog, Switcher

class ExportPrintDialog(XDialog):
    def __init__(self):
        super().__init__()

        self.dia_state = DialogState()
        self.export_state = ExportState()
        self.r_state = RenderState()
        self.r_state.on_image_change = self.update_preview
        self.ad_state = AnimationDisableState()
        self.ad_state.on_change = self.update_animations

        self.content_padding = 0
        self.title_padding = 0
        self.elevation = 0
        self.clip_behavior = ClipBehavior.HARD_EDGE
        self.bgcolor = "#ededed"
        self.actions_padding = padding.all(16)
        self.action_button_padding = 0
        self.actions_overflow_button_spacing = 0
        self.open_duration = 300 if self.ad_state.state else 0
        self.modal = True

        self.print_export_setting = Switcher(
            orientation=Switcher.Orientation.HORIZONTAL,
            expand = True,
            controls = [
                Container(
                    expand = True,
                    content = Row(
                        expand = True,
                        controls = [
                            Text("File Format:", expand=True),
                            DropdownM2(
                                "pdf",
                                expand = True,
                                options=[
                                    DropdownOption(
                                        "pdf",
                                        "PDF",
                                        text_style=TextStyle(size=16)
                                    ),
                                    DropdownOption(
                                        "png",
                                        "PNG",
                                        text_style=TextStyle(size=16)
                                    ),
                                    DropdownOption(
                                        "docx",
                                        "DOCX",
                                        text_style=TextStyle(size=16)
                                    ),
                                    DropdownOption(
                                        "raw_png",
                                        "RAW_PNG",
                                        text_style=TextStyle(size=16)
                                    ),
                                ],
                                on_change = self.update_format
                            )
                        ]
                    )
                ),
                Container(
                    expand = True,
                    content = Row(
                        expand = True,
                        controls = [
                            Text("Page Size:", expand=True),
                            DropdownM2(
                                "letter",
                                expand = True,
                                text_style=TextStyle(size=14, color="black"),
                                options=[
                                    DropdownOption(
                                        "letter",
                                        "Letter 8.5 x 14 in",
                                        text_style=TextStyle(size=12, color="black")
                                    ),
                                    DropdownOption(
                                        "folio",
                                        "Folio 8.5 x 13 in",
                                        text_style=TextStyle(size=12, color="black")
                                    ),
                                    DropdownOption(
                                        "legal",
                                        "Legal 8.5 x 14 in",
                                        text_style=TextStyle(size=12, color="black")
                                    ),
                                    DropdownOption(
                                        "a4",
                                        "A4 8.3 x 11.7 in",
                                        text_style=TextStyle(size=12, color="black")
                                    ),
                                    DropdownOption(
                                        "b4",
                                        "B4 9.8 x 13.9 in",
                                        text_style=TextStyle(size=12, color="black")
                                    ),
                                ]
                            )
                        ]
                    )
                )
            ]
        )

        self.export_button = FilledButton(
            "Export", 
            expand=True,
            disabled=True,
            on_click= lambda e: self.export_state.export() if e.control.text == "Export" else print("HAHA")
        )

        self.print_button = FilledButton(
            "Print", 
            expand=True,
            disabled=True,
            on_click= lambda e: self.export_state.export() if e.control.text == "Print" else print("HAHA")
        )

        self.project_name_tf = TextField(
            hint_text="e.g. Xilogism 1",
            expand=True,
            text_size=14,
            content_padding=padding.symmetric(8, 12),
            on_change= self.update_fields
        )

        self.creator_tf = TextField(
            hint_text="e.g. User",
            expand=True,
            text_size=14,
            content_padding=padding.symmetric(8, 12),
            on_change= self.update_fields
        )

        self.date_tf = TextField(
            hint_text="e.g. 04/07/2025",
            expand=True,
            text_size=14,
            content_padding=padding.symmetric(8, 12),
            on_change= self.update_fields
        )

        self.extra_options = Revealer(
            height=150,
            orientation=Revealer.Orientation.VERTICAL,
            content = Container(
                height=150,
                padding = padding.symmetric(8, 24),
                border = border.all(1, "#73191f51"),
                border_radius = 8,
                content = Column(
                    scroll = ScrollMode.HIDDEN,
                    controls = [
                        Row(
                            expand = True,
                            height=36,
                            controls = [
                                Text("Project Name:", expand=True),
                                self.project_name_tf
                            ]
                        ),
                        Row(
                            expand = True,
                            height=36,
                            controls = [
                                Text("Creator :", expand=True),
                                self.creator_tf
                            ]
                        ),
                        Row(
                            expand = True,
                            height=36,
                            controls = [
                                Text("Date:", expand=True),
                                self.date_tf
                            ]
                        )
                    ]
                )
            )
        )

        self.margin_switch = Switch("", value=True, on_change = self.update_margin)
        self.titleblock_switch = Switch("", value=True, on_change = self.update_titleblock)

        self.main_options = Container(
            expand=True,
            padding=padding.symmetric(8, 0),
            content = Column(
                expand = True,
                controls = [
                    self.print_export_setting,
                    Row(
                        controls = [
                            Text("Margin:", expand=True),
                            Row(
                                expand = True,
                                controls = [
                                    self.margin_switch
                                ]
                            )
                        ]
                    ),
                    Row(
                        controls = [
                            Text("Title Block:", expand=True),
                            Row(
                                expand=True,
                                alignment=MainAxisAlignment.START,
                                controls = [
                                    self.titleblock_switch
                                ]
                            )
                        ],
                        alignment=MainAxisAlignment.START
                    ),
                    self.extra_options,
                    Container(
                        padding = padding.symmetric(0, 8),
                        content = Row(
                            controls = [
                                self.export_button,
                                self.print_button,
                                FilledButton(
                                    "Cancel", 
                                    expand=True,
                                    bgcolor="#73ff0000",
                                    on_click=lambda e: setattr(self.dia_state, 'state', Dialogs.CLOSE)
                                )
                            ],
                            alignment=MainAxisAlignment.START
                        )
                    )
                ]
            )
        )

        self.preview_image = Image(
            width=360,
            height=240
        )

        self.content=Container(
            padding = 8,
            height=500,
            width=1024,
            expand=True,
            content = Column(
                horizontal_alignment=CrossAxisAlignment.STRETCH,
                controls=[
                    Container(
                        padding = padding.only(left=16, bottom=0, right=16, top=16),
                        expand=True,
                        content = Row(
                            expand=True,
                            spacing = 0,
                            controls = [
                                Column(
                                    expand = True,
                                    spacing = 16,
                                    controls = [
                                        Text("Export Xilogism", size=24, weight=FontWeight.BOLD),
                                        Container(
                                            content = self.preview_image,
                                            width = 420,
                                            height = 300,
                                            margin = margin.only(top=48),
                                            border_radius=8,
                                            border=border.all(1, "black"),
                                            alignment=alignment.center,
                                            image=DecorationImage(
                                                src="export_sample_bg.png"
                                            )
                                        )
                                    ]
                                ),
                                Container(
                                    expand = True,
                                    padding = padding.only(top = 48),
                                    content = Column(
                                        expand=True,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        controls = [
                                            self.main_options
                                        ]
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
    
    def update_animations(self):
        animate = self.ad_state.state
        self.open_duration = 300 if animate else 0
        self.print_export_setting.animation_duration = 300 if animate else 25
        self.extra_options.animation_duration = 500 if animate else 0
        self.update()
    
    def update_titleblock(self, event: ControlEvent):
        self.export_state.titleblock_enable = (event.data == "true")

        if event.data == "true" and all([self.project_name_tf.value != "", self.creator_tf.value != "", self.date_tf.value != ""]):
            self.export_button.disabled = False
            self.print_button.disabled = False
        elif event.data == "false":
            self.export_button.disabled = False
            self.print_button.disabled = False
        else:
            self.export_button.disabled = True
            self.print_button.disabled = True

        self.print_button.update()
        self.export_button.update()

        self.extra_options.content_hidden = not self.extra_options.content_hidden
        self.extra_options.update()
    
    def update_preview(self, image_dict: dict):
        self.preview_image.src_base64 = list(image_dict.values())[0]
        self.preview_image.update()
    
    def update_format(self, event: ControlEvent):
        match event.data:
            case "png":
                self.export_state.format = FileFormat.PNG
                self.disable_buttons(False)
                self.export_button.disabled = True
                self.print_button.disabled = True
            case "pdf":
                self.export_state.format = FileFormat.PDF
                self.disable_buttons(False)
                self.export_button.disabled = True
                self.print_button.disabled = True
            case "docx":
                self.export_state.format = FileFormat.DOCX
                self.disable_buttons(False)
                self.export_button.disabled = True
                self.print_button.disabled = True
            case "raw_png":
                self.export_state.format = FileFormat.RAW_PNG
                self.disable_buttons(True)
                self.export_button.disabled = False
                self.print_button.disabled = False

        self.print_button.update()
        self.export_button.update()
    
    def disable_buttons(self, state: bool):
        self.margin_switch.disabled = state
        self.titleblock_switch.disabled = state
        self.project_name_tf.disabled = state
        self.creator_tf.disabled = state
        self.date_tf.disabled = state

        self.update()
    
    def update_margin(self, event: ControlEvent):
        self.export_state.margin = (event.data == "true")
        self.export_button.disabled = not (event.data == "true")
        self.export_button.update()
        self.print_button.disabled = not (event.data == "true")
        self.print_button.update()
    
    def update_fields(self, event: ControlEvent):
        if all([self.project_name_tf.value != "", self.creator_tf.value != "", self.date_tf.value != ""]):
            self.export_button.disabled = False
            self.print_button.disabled = False

            self.export_state.proj_name = self.project_name_tf.value
            self.export_state.creator = self.creator_tf.value
            self.export_state.date = self.date_tf.value
        else:
            self.export_button.disabled = True
            self.print_button.disabled = True

        self.export_button.update()
        self.print_button.update()